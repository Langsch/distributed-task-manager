# API Documentation

## Coordinator Service (Computer 1 - Port 8000)

Base URL: `http://localhost:8000`

### System Information

#### GET /
Get system overview and health status.

**Response:**
```json
{
  "service": "University Management Coordinator",
  "status": "running",
  "statistics": {
    "total_universities": 4,
    "total_courses": 7,
    "active_students": 15,
    "universities_with_students": 3
  },
  "active_workers": 1,
  "total_workers": 1
}
```

#### GET /stats
Get detailed system statistics.

**Response:**
```json
{
  "universities_by_type": [
    {"type": "public", "count": 3, "avg_students": 47333.33},
    {"type": "private", "count": 1, "avg_students": 23000.0}
  ],
  "courses_by_area": [
    {"area": "Exatas", "count": 3, "avg_duration": 4.0},
    {"area": "Saúde", "count": 1, "avg_duration": 6.0}
  ],
  "students_by_year": [
    {"enrollment_year": 2024, "count": 10},
    {"enrollment_year": 2023, "count": 5}
  ],
  "worker_nodes": [...]
}
```

### Worker Management

#### GET /workers
List all registered worker nodes.

**Response:**
```json
{
  "workers": [
    {
      "node_id": "worker-abc123",
      "host": "192.168.1.101",
      "port": 8001,
      "status": "active",
      "capabilities": ["students", "analytics", "validation"]
    }
  ]
}
```

#### POST /workers/register
Register a new worker node.

**Request Body:**
```json
{
  "node_id": "worker-xyz789",
  "host": "192.168.1.102",
  "port": 8001,
  "status": "active",
  "capabilities": ["students", "analytics"]
}
```

**Response:**
```json
{
  "message": "Worker registered successfully",
  "node_id": "worker-xyz789"
}
```

#### DELETE /workers/{node_id}
Unregister a worker node.

**Response:**
```json
{
  "message": "Worker unregistered"
}
```

### University Management

#### GET /universities
List all universities with student counts.

**Response:**
```json
{
  "universities": [
    {
      "id": 1,
      "name": "UFRJ",
      "state": "RJ",
      "type": "public",
      "founded_year": 1920,
      "student_count": 45000,
      "current_students": 25
    }
  ]
}
```

#### POST /universities
Create a new university.

**Request Body:**
```json
{
  "name": "MIT",
  "state": "MA",
  "type": "private",
  "founded_year": 1861,
  "student_count": 11000
}
```

**Response:**
```json
{
  "id": 5,
  "message": "University created successfully"
}
```

#### GET /universities/{university_id}
Get detailed university information.

**Response:**
```json
{
  "university": {
    "id": 1,
    "name": "UFRJ",
    "state": "RJ",
    "type": "public",
    "founded_year": 1920,
    "student_count": 45000
  },
  "courses": [
    {
      "id": 1,
      "name": "Ciência da Computação",
      "duration_years": 4,
      "area": "Exatas",
      "annual_spots": 50,
      "tuition_fee": 0.0
    }
  ],
  "student_statistics": [
    {
      "course_name": "Ciência da Computação",
      "student_count": 15
    }
  ]
}
```

### Course Management

#### GET /courses
List all courses with statistics.

**Response:**
```json
{
  "courses": [
    {
      "id": 1,
      "name": "Ciência da Computação",
      "duration_years": 4,
      "area": "Exatas",
      "universities_offering": 2,
      "total_students": 20
    }
  ]
}
```

#### POST /courses
Create a new course.

**Request Body:**
```json
{
  "name": "Engenharia de Dados",
  "duration_years": 4,
  "area": "Exatas"
}
```

**Response:**
```json
{
  "id": 8,
  "message": "Course created successfully"
}
```

### Student Management (Distributed)

#### GET /students
List all students with university and course information.

**Response:**
```json
{
  "students": [
    {
      "id": 1,
      "name": "João Silva",
      "email": "joao@example.com",
      "university_id": 1,
      "course_id": 1,
      "enrollment_year": 2024,
      "status": "active",
      "university_name": "UFRJ",
      "course_name": "Ciência da Computação"
    }
  ]
}
```

#### POST /students
Create a new student (delegated to worker if available).

**Request Body:**
```json
{
  "name": "Maria Santos",
  "email": "maria@example.com",
  "university_id": 1,
  "course_id": 1,
  "enrollment_year": 2024
}
```

**Response (when processed by worker):**
```json
{
  "success": true,
  "data": {
    "id": 1234,
    "student_data": {...},
    "validation": {
      "student_id": "STU20241234",
      "email_verified": true,
      "enrollment_valid": true,
      "enriched_data": {
        "academic_level": "undergraduate",
        "estimated_graduation": 2028,
        "semester": 2
      }
    },
    "message": "Student processed successfully"
  },
  "processing_time": 1.23,
  "worker_id": "worker-abc123"
}
```

## Worker Service (Computer 2 - Port 8001)

Base URL: `http://localhost:8001`

### Worker Information

#### GET /
Get worker service information.

**Response:**
```json
{
  "service": "University Management Worker",
  "worker_id": "worker-abc123",
  "status": "running",
  "coordinator_url": "http://192.168.1.100:8000",
  "capabilities": ["students", "analytics", "validation"],
  "uptime_seconds": 3600.5
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "worker_id": "worker-abc123",
  "status": "healthy",
  "hostname": "computer-2",
  "local_ip": "192.168.1.101",
  "memory_usage": "normal",
  "cpu_usage": "low"
}
```

#### GET /stats
Get worker statistics.

**Response:**
```json
{
  "worker_id": "worker-abc123",
  "uptime_seconds": 3600.5,
  "uptime_formatted": "1h 0m",
  "students_processed": 15,
  "total_requests": 18,
  "errors": 1,
  "success_rate": 0.94,
  "recent_requests": 3
}
```

### Processing Endpoints

#### POST /process_student
Process student creation with validation and enrichment.

**Request Body:**
```json
{
  "name": "Pedro Costa",
  "email": "pedro@example.com",
  "university_id": 2,
  "course_id": 3,
  "enrollment_year": 2024
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 5678,
    "student_data": {...},
    "validation": {
      "student_id": "STU20245678",
      "email_verified": true,
      "enrollment_valid": true,
      "processing_timestamp": "2024-06-28T15:30:45",
      "enriched_data": {
        "academic_level": "undergraduate",
        "estimated_graduation": 2028,
        "semester": 2
      }
    },
    "message": "Student processed successfully"
  },
  "processing_time": 0.89,
  "worker_id": "worker-abc123"
}
```

#### POST /analytics/students
Generate student analytics.

**Request Body:**
```json
{
  "university_id": 1,
  "course_id": 1,
  "year_range": 5
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "university_id": 1,
    "course_id": 1,
    "period_analyzed": "2020-2025",
    "enrollment_trends": {
      "2020": 45,
      "2021": 52,
      "2022": 48,
      "2023": 67,
      "2024": 73,
      "2025": 81
    },
    "retention_rate": 0.87,
    "graduation_rate": 0.82,
    "average_grade": 8.2,
    "employment_rate": 0.91,
    "generated_at": "2024-06-28T15:35:12"
  },
  "processing_time": 1.45,
  "worker_id": "worker-abc123"
}
```

### Monitoring Endpoints

#### GET /processed_requests
Get recent processed requests.

**Response:**
```json
{
  "worker_id": "worker-abc123",
  "total_processed": 15,
  "recent_requests": [
    {
      "request_id": "req-123",
      "student_name": "Ana Silva",
      "processing_time": 0.95,
      "timestamp": "2024-06-28T15:20:30",
      "result": {...}
    }
  ]
}
```

### Test Endpoints

#### POST /test/student
Create a test student for demonstration.

**Response:**
```json
{
  "success": true,
  "data": {
    "student_data": {
      "name": "João Silva",
      "email": "joao.silva@example.com",
      "university_id": 1,
      "course_id": 1,
      "enrollment_year": 2024
    },
    "validation": {...}
  },
  "processing_time": 1.12,
  "worker_id": "worker-abc123"
}
```

#### POST /test/analytics
Generate test analytics for demonstration.

**Response:**
```json
{
  "success": true,
  "data": {
    "university_id": 1,
    "course_id": 1,
    "enrollment_trends": {...},
    "retention_rate": 0.89
  },
  "processing_time": 1.78,
  "worker_id": "worker-abc123"
}
```

## Error Responses

All endpoints return appropriate HTTP status codes:
- `200 OK`: Successful operation
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Error Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting and Performance

- No rate limiting implemented (educational project)
- Average response time: < 2 seconds
- Concurrent request handling supported
- Async processing for improved performance
