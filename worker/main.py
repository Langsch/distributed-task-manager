from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uuid
import socket
import time
import random
import sys
from datetime import datetime

app = FastAPI(
    title="University Management Worker", 
    description="Distributed University Management System - Worker Node",
    version="1.0.0"
)

# Worker configuration
WORKER_ID = f"worker-{str(uuid.uuid4())[:8]}"

# Import configuration
sys.path.append('..')
try:
    from config import COORDINATOR_IP, COORDINATOR_PORT, WORKER_HOST, WORKER_PORT
    COORDINATOR_URL = f"http://{COORDINATOR_IP}:{COORDINATOR_PORT}"
except ImportError:
    # Fallback if config.py not found
    COORDINATOR_URL = "http://192.168.1.100:8000"  # Update with Computer 1 IP
    WORKER_HOST = "0.0.0.0"
    WORKER_PORT = 8001

# Worker state
processed_requests = []
worker_stats = {
    "students_processed": 0,
    "requests_handled": 0,
    "uptime_start": time.time(),
    "errors": 0
}

# Models
class StudentCreate(BaseModel):
    name: str
    email: str
    university_id: int
    course_id: int
    enrollment_year: int

class StudentAnalytics(BaseModel):
    university_id: int
    course_id: int
    year_range: int = 5

class ProcessingResult(BaseModel):
    success: bool
    data: Dict[str, Any]
    processing_time: float
    worker_id: str

# Student Processing Functions
def validate_student_data(student: StudentCreate) -> Dict[str, Any]:
    """Validate and enrich student data"""
    print(f"Processing student: {student.name}")
    
    # Simulate validation and enrichment
    time.sleep(random.uniform(0.5, 1.5))
    
    # Generate student ID and additional data
    student_id = f"STU{student.enrollment_year}{random.randint(1000, 9999)}"
    
    # Simulate validation checks
    validation_result = {
        "student_id": student_id,
        "email_verified": "@" in student.email and "." in student.email,
        "enrollment_valid": 2020 <= student.enrollment_year <= 2025,
        "processing_timestamp": datetime.now().isoformat(),
        "enriched_data": {
            "academic_level": "undergraduate" if student.enrollment_year >= 2022 else "senior",
            "estimated_graduation": student.enrollment_year + 4,
            "semester": 1 if datetime.now().month <= 6 else 2
        }
    }
    
    return validation_result

def generate_student_analytics(analytics_request: StudentAnalytics) -> Dict[str, Any]:
    """Generate analytics for students"""
    print(f"Generating analytics for university {analytics_request.university_id}")
    
    # Simulate analytics processing
    time.sleep(random.uniform(1, 2))
    
    # Generate fake analytics data
    current_year = datetime.now().year
    years = list(range(current_year - analytics_request.year_range, current_year + 1))
    
    analytics = {
        "university_id": analytics_request.university_id,
        "course_id": analytics_request.course_id,
        "period_analyzed": f"{min(years)}-{max(years)}",
        "enrollment_trends": {
            str(year): random.randint(20, 100) for year in years
        },
        "retention_rate": round(random.uniform(0.75, 0.95), 2),
        "graduation_rate": round(random.uniform(0.70, 0.90), 2),
        "average_grade": round(random.uniform(7.0, 9.5), 1),
        "employment_rate": round(random.uniform(0.80, 0.95), 2),
        "generated_at": datetime.now().isoformat()
    }
    
    return analytics

# Main Processing Endpoints
@app.post("/process_student")
async def process_student(student: StudentCreate):
    """Process student creation with validation and enrichment"""
    start_time = time.time()
    
    try:
        # Process student data
        validation_result = validate_student_data(student)
        
        # Simulate database insertion (in real scenario, worker might have its own DB)
        processing_time = time.time() - start_time
        
        # Update stats
        worker_stats["students_processed"] += 1
        worker_stats["requests_handled"] += 1
        
        # Store processing record
        processing_record = {
            "request_id": str(uuid.uuid4()),
            "student_name": student.name,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat(),
            "result": validation_result
        }
        processed_requests.append(processing_record)
        
        # Prepare response
        result = ProcessingResult(
            success=True,
            data={
                "id": random.randint(1000, 9999),  # Simulated DB ID
                "student_data": student.dict(),
                "validation": validation_result,
                "message": "Student processed successfully"
            },
            processing_time=processing_time,
            worker_id=WORKER_ID
        )
        
        print(f"Successfully processed student {student.name} in {processing_time:.2f}s")
        return result.dict()
        
    except Exception as e:
        worker_stats["errors"] += 1
        worker_stats["requests_handled"] += 1
        
        processing_time = time.time() - start_time
        
        result = ProcessingResult(
            success=False,
            data={"error": str(e), "student_data": student.dict()},
            processing_time=processing_time,
            worker_id=WORKER_ID
        )
        
        print(f"Error processing student {student.name}: {e}")
        return result.dict()

@app.post("/analytics/students")
async def generate_analytics(analytics_request: StudentAnalytics):
    """Generate student analytics"""
    start_time = time.time()
    
    try:
        analytics_data = generate_student_analytics(analytics_request)
        processing_time = time.time() - start_time
        
        worker_stats["requests_handled"] += 1
        
        result = ProcessingResult(
            success=True,
            data=analytics_data,
            processing_time=processing_time,
            worker_id=WORKER_ID
        )
        
        return result.dict()
        
    except Exception as e:
        worker_stats["errors"] += 1
        processing_time = time.time() - start_time
        
        result = ProcessingResult(
            success=False,
            data={"error": str(e)},
            processing_time=processing_time,
            worker_id=WORKER_ID
        )
        
        return result.dict()

# Worker Information Endpoints
@app.get("/")
async def root():
    """Worker information"""
    return {
        "service": "University Management Worker",
        "worker_id": WORKER_ID,
        "status": "running",
        "coordinator_url": COORDINATOR_URL,
        "capabilities": ["students", "analytics", "validation"],
        "uptime_seconds": time.time() - worker_stats["uptime_start"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "worker_id": WORKER_ID,
        "status": "healthy",
        "hostname": socket.gethostname(),
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "memory_usage": "normal",  # Simulated
        "cpu_usage": "low"  # Simulated
    }

@app.get("/stats")
async def get_worker_stats():
    """Get worker statistics"""
    uptime = time.time() - worker_stats["uptime_start"]
    
    return {
        "worker_id": WORKER_ID,
        "uptime_seconds": uptime,
        "uptime_formatted": f"{uptime//3600:.0f}h {(uptime%3600)//60:.0f}m",
        "students_processed": worker_stats["students_processed"],
        "total_requests": worker_stats["requests_handled"],
        "errors": worker_stats["errors"],
        "success_rate": round((worker_stats["requests_handled"] - worker_stats["errors"]) / max(worker_stats["requests_handled"], 1), 2),
        "recent_requests": len([r for r in processed_requests if (time.time() - time.mktime(time.strptime(r["timestamp"][:19], "%Y-%m-%dT%H:%M:%S"))) < 300])
    }

@app.get("/processed_requests")
async def get_processed_requests():
    """Get recent processed requests"""
    return {
        "worker_id": WORKER_ID,
        "total_processed": len(processed_requests),
        "recent_requests": processed_requests[-10:] if processed_requests else []  # Last 10
    }

# Test endpoints for demonstration
@app.post("/test/student")
async def test_student_processing():
    """Test endpoint to create a sample student"""
    test_student = StudentCreate(
        name="João Silva",
        email="joao.silva@example.com",
        university_id=1,
        course_id=1,
        enrollment_year=2024
    )
    
    return await process_student(test_student)

@app.post("/test/analytics")
async def test_analytics():
    """Test endpoint for analytics"""
    test_analytics = StudentAnalytics(
        university_id=1,
        course_id=1,
        year_range=5
    )
    
    return await generate_analytics(test_analytics)

# Startup event - Register with coordinator
@app.on_event("startup")
async def startup_event():
    """Register with coordinator on startup"""
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        
        registration_data = {
            "node_id": WORKER_ID,
            "host": local_ip,
            "port": WORKER_PORT,
            "status": "active",
            "capabilities": ["students", "analytics", "validation"]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{COORDINATOR_URL}/workers/register",
                json=registration_data,
                timeout=10.0
            )
        
        if response.status_code == 200:
            print(f"✅ Successfully registered worker {WORKER_ID} with coordinator")
        else:
            print(f"❌ Failed to register with coordinator: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  Could not register with coordinator: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=WORKER_HOST, port=WORKER_PORT)
