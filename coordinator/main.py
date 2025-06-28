from typing import Literal, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from datetime import datetime
import httpx
import asyncio

from database import get_engine, init_db

# Initialize database
init_db()
engine = get_engine()

app = FastAPI(
    title="University Management Coordinator", 
    description="Distributed University Management System - Main Server",
    version="1.0.0"
)

# Worker nodes registry
worker_nodes = []

# Pydantic Models
class UniversityCreate(BaseModel):
    name: str
    state: str
    type: Literal['public', 'private']
    founded_year: Optional[int] = None
    student_count: Optional[int] = 0

class CourseCreate(BaseModel):
    name: str
    duration_years: int = 4
    area: str

class StudentCreate(BaseModel):
    name: str
    email: str
    university_id: int
    course_id: int
    enrollment_year: int

class WorkerNode(BaseModel):
    node_id: str
    host: str
    port: int
    status: Literal["active", "inactive"]
    capabilities: List[str]

# Worker Management Endpoints
@app.post("/workers/register")
async def register_worker(worker: WorkerNode):
    """Register a worker node"""
    for existing_worker in worker_nodes:
        if existing_worker["node_id"] == worker.node_id:
            existing_worker.update(worker.dict())
            return {"message": "Worker updated", "node_id": worker.node_id}
    
    worker_nodes.append(worker.dict())
    return {"message": "Worker registered successfully", "node_id": worker.node_id}

@app.get("/workers")
async def get_workers():
    """Get all registered workers"""
    return {"workers": worker_nodes}

@app.delete("/workers/{node_id}")
async def unregister_worker(node_id: str):
    """Unregister a worker node"""
    global worker_nodes
    worker_nodes = [w for w in worker_nodes if w["node_id"] != node_id]
    return {"message": "Worker unregistered"}

# University Management
@app.get("/universities")
def get_universities():
    """Get all universities"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT u.*, COUNT(s.id) as current_students
            FROM university u
            LEFT JOIN student s ON u.id = s.university_id AND s.status = 'active'
            GROUP BY u.id
            ORDER BY u.name
        """))
        universities = result.mappings().all()
    
    return {"universities": [dict(u) for u in universities]}

@app.post("/universities")
def create_university(university: UniversityCreate):
    """Create a new university"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            INSERT INTO university (name, state, type, founded_year, student_count)
            VALUES (:name, :state, :type, :founded_year, :student_count)
            RETURNING id
        """), university.dict())
        
        university_id = result.scalar()
    
    return {"id": university_id, "message": "University created successfully"}

@app.get("/universities/{university_id}")
def get_university(university_id: int):
    """Get specific university with details"""
    with engine.begin() as conn:
        # Get university info
        university_result = conn.execute(text("""
            SELECT * FROM university WHERE id = :id
        """), {"id": university_id})
        
        university = university_result.mappings().first()
        if not university:
            raise HTTPException(status_code=404, detail="University not found")
        
        # Get courses offered
        courses_result = conn.execute(text("""
            SELECT c.*, uc.annual_spots, uc.tuition_fee
            FROM course c
            JOIN university_course uc ON c.id = uc.course_id
            WHERE uc.university_id = :id
        """), {"id": university_id})
        
        courses = courses_result.mappings().all()
        
        # Get student count by course
        students_result = conn.execute(text("""
            SELECT c.name as course_name, COUNT(s.id) as student_count
            FROM course c
            JOIN student s ON c.id = s.course_id
            WHERE s.university_id = :id AND s.status = 'active'
            GROUP BY c.id, c.name
        """), {"id": university_id})
        
        student_stats = students_result.mappings().all()
    
    return {
        "university": dict(university),
        "courses": [dict(c) for c in courses],
        "student_statistics": [dict(s) for s in student_stats]
    }

# Course Management
@app.get("/courses")
def get_courses():
    """Get all courses"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT c.*, COUNT(DISTINCT uc.university_id) as universities_offering,
                   COUNT(s.id) as total_students
            FROM course c
            LEFT JOIN university_course uc ON c.id = uc.course_id
            LEFT JOIN student s ON c.id = s.course_id AND s.status = 'active'
            GROUP BY c.id
            ORDER BY c.area, c.name
        """))
        courses = result.mappings().all()
    
    return {"courses": [dict(c) for c in courses]}

@app.post("/courses")
def create_course(course: CourseCreate):
    """Create a new course"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            INSERT INTO course (name, duration_years, area)
            VALUES (:name, :duration_years, :area)
            RETURNING id
        """), course.dict())
        
        course_id = result.scalar()
    
    return {"id": course_id, "message": "Course created successfully"}

# Student Management (Distributed to Worker)
@app.post("/students")
async def create_student(student: StudentCreate):
    """Create a new student (delegated to worker if available)"""
    # Try to delegate to worker
    available_workers = [w for w in worker_nodes if w["status"] == "active" and "students" in w["capabilities"]]
    
    if available_workers:
        worker = available_workers[0]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://{worker['host']}:{worker['port']}/process_student",
                    json=student.dict(),
                    timeout=10.0
                )
                
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Worker delegation failed: {e}")
    
    # Fallback: process locally
    with engine.begin() as conn:
        # Verify university and course exist
        verification = conn.execute(text("""
            SELECT u.name as university_name, c.name as course_name
            FROM university u, course c
            WHERE u.id = :university_id AND c.id = :course_id
        """), {"university_id": student.university_id, "course_id": student.course_id})
        
        if not verification.first():
            raise HTTPException(status_code=400, detail="Invalid university or course ID")
        
        result = conn.execute(text("""
            INSERT INTO student (name, email, university_id, course_id, enrollment_year)
            VALUES (:name, :email, :university_id, :course_id, :enrollment_year)
            RETURNING id
        """), student.dict())
        
        student_id = result.scalar()
    
    return {"id": student_id, "message": "Student created successfully", "processed_by": "coordinator"}

@app.get("/students")
def get_students():
    """Get all students"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT s.*, u.name as university_name, c.name as course_name
            FROM student s
            JOIN university u ON s.university_id = u.id
            JOIN course c ON s.course_id = c.id
            ORDER BY s.name
        """))
        students = result.mappings().all()
    
    return {"students": [dict(s) for s in students]}

# Statistics and Health
@app.get("/")
async def root():
    """System overview"""
    with engine.begin() as conn:
        stats = conn.execute(text("""
            SELECT 
                (SELECT COUNT(*) FROM university) as total_universities,
                (SELECT COUNT(*) FROM course) as total_courses,
                (SELECT COUNT(*) FROM student WHERE status = 'active') as active_students,
                (SELECT COUNT(DISTINCT university_id) FROM student) as universities_with_students
        """)).mappings().first()
    
    return {
        "service": "University Management Coordinator",
        "status": "running",
        "statistics": dict(stats),
        "active_workers": len([w for w in worker_nodes if w["status"] == "active"]),
        "total_workers": len(worker_nodes)
    }

@app.get("/stats")
def get_detailed_stats():
    """Detailed system statistics"""
    with engine.begin() as conn:
        # Universities by type
        uni_stats = conn.execute(text("""
            SELECT type, COUNT(*) as count, AVG(student_count) as avg_students
            FROM university
            GROUP BY type
        """)).mappings().all()
        
        # Courses by area
        course_stats = conn.execute(text("""
            SELECT area, COUNT(*) as count, AVG(duration_years) as avg_duration
            FROM course
            GROUP BY area
        """)).mappings().all()
        
        # Students by enrollment year
        student_stats = conn.execute(text("""
            SELECT enrollment_year, COUNT(*) as count
            FROM student
            WHERE status = 'active'
            GROUP BY enrollment_year
            ORDER BY enrollment_year DESC
        """)).mappings().all()
    
    return {
        "universities_by_type": [dict(s) for s in uni_stats],
        "courses_by_area": [dict(s) for s in course_stats],
        "students_by_year": [dict(s) for s in student_stats],
        "worker_nodes": worker_nodes
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
