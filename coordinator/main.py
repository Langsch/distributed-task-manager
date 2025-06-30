"""
University Management API

FastAPI-based REST API for managing universities and their courses.
Designed for distributed client-server architecture.
"""

from typing import Literal, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text

from database import get_engine, init_db

init_db()
engine = get_engine()

app = FastAPI(
    title="University Management API", 
    description="Simple University Management System",
    version="1.0.0"
)

UNIVERSITY_NOT_FOUND = "University not found"
SELECT_UNIVERSITY_BY_ID = """
    SELECT id FROM university WHERE id = :id
"""
class UniversityCreate(BaseModel):
    name: str
    state: str
    type: Literal['public', 'private']

class UniversityUpdate(BaseModel):
    name: str
    state: str
    type: Literal['public', 'private']

class CourseAssignment(BaseModel):
    courses: List[int]

class Course(BaseModel):
    id: int
    name: str

class University(BaseModel):
    id: int
    name: str
    state: str
    type: str
    courses: List[Course] = []

@app.get("/universities")
def get_universities():
    """Get all universities"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT *
            FROM university
            ORDER BY name
        """))
        universities = result.mappings().all()
    
    return {"universities": universities}

@app.post("/universities")
def create_university(university: UniversityCreate):
    """Create a new university"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            INSERT INTO university (name, state, type)
            VALUES (:name, :state, :type)
            RETURNING id
        """), {
            "name": university.name,
            "state": university.state,
            "type": university.type
        })
        
        university_id = result.scalar()
    
    return {"id": university_id}

@app.get("/universities/{id}")
def get_university(id: int):
    """Get university details with courses"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT * FROM university WHERE id = :id
        """), {"id": id})
        university = result.mappings().first()
        
        if not university:
            raise HTTPException(status_code=404, detail=UNIVERSITY_NOT_FOUND)
        
        result = conn.execute(text("""
            SELECT c.id, c.name 
            FROM course c
            JOIN university_course uc ON c.id = uc.course_id
            WHERE uc.university_id = :id
            ORDER BY c.name
        """), {"id": id})
        courses = result.mappings().all()
        
        return {
            "id": university["id"],
            "name": university["name"],
            "state": university["state"],
            "type": university["type"],
            "courses": [{"id": c["id"], "name": c["name"]} for c in courses]
        }

@app.put("/universities/{id}")
def update_university(id: int, university: UniversityUpdate):
    """Update university details"""
    with engine.begin() as conn:
        result = conn.execute(text(SELECT_UNIVERSITY_BY_ID), {"id": id})
        
        if not result.first():
            raise HTTPException(status_code=404, detail=UNIVERSITY_NOT_FOUND)
        
        conn.execute(text("""
            UPDATE university 
            SET name = :name, state = :state, type = :type
            WHERE id = :id
        """), {
            "id": id,
            "name": university.name,
            "state": university.state,
            "type": university.type
        })
    
    return {"message": "University updated successfully"}

@app.delete("/universities/{id}")
def delete_university(id: int):
    """Delete university"""
    with engine.begin() as conn:
        result = conn.execute(text(SELECT_UNIVERSITY_BY_ID), {"id": id})
        
        if not result.first():
            raise HTTPException(status_code=404, detail=UNIVERSITY_NOT_FOUND)
        
        conn.execute(text("""
            DELETE FROM university_course WHERE university_id = :id
        """), {"id": id})
        
        conn.execute(text("""
            DELETE FROM university WHERE id = :id
        """), {"id": id})
    
    return {"message": "University deleted successfully"}

@app.put("/universities/{id}/courses")
def assign_courses(id: int, assignment: CourseAssignment):
    """Assign courses to university"""
    with engine.begin() as conn:
        result = conn.execute(text(SELECT_UNIVERSITY_BY_ID), {"id": id})
        
        if not result.first():
            raise HTTPException(status_code=404, detail=UNIVERSITY_NOT_FOUND)
        
        if assignment.courses:
            placeholders = ",".join([":course" + str(i) for i in range(len(assignment.courses))])
            params = {"course" + str(i): course_id for i, course_id in enumerate(assignment.courses)}
            
            result = conn.execute(text(f"""
                SELECT COUNT(*) as count FROM course WHERE id IN ({placeholders})
            """), params)
            
            if result.scalar() != len(assignment.courses):
                raise HTTPException(status_code=400, detail="One or more course IDs are invalid")
        
        conn.execute(text("""
            DELETE FROM university_course WHERE university_id = :id
        """), {"id": id})
        
        for course_id in assignment.courses:
            conn.execute(text("""
                INSERT INTO university_course (university_id, course_id)
                VALUES (:university_id, :course_id)
            """), {"university_id": id, "course_id": course_id})
    
    return {"message": "Courses assigned successfully"}

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
