# University Management API Documentation

REST API for managing universities and their courses in a distributed system.

## Base URL

- **Local:** `http://localhost:8000`
- **Distributed:** `http://COMPUTER1_IP:8000` (replace with Computer 1's actual IP)

## Authentication

No authentication required (demo system).

## Common Headers

```
Content-Type: application/json
Accept: application/json
```

## API Endpoints

### Health Check

#### GET /health
Get API health status.

**Response:**
```json
{
  "status": "healthy"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### Universities

#### GET /universities
Get all universities.

**Response:**
```json
{
  "universities": [
    {
      "id": 1,
      "name": "UFRJ",
      "state": "RJ",
      "type": "public"
    },
    {
      "id": 2,
      "name": "PUC-Rio", 
      "state": "RJ",
      "type": "private"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/universities
```

#### POST /universities
Create a new university.

**Request Body:**
```json
{
  "name": "string",
  "state": "string", 
  "type": "public" | "private"
}
```

**Response:**
```json
{
  "id": 5
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/universities \
  -H "Content-Type: application/json" \
  -d '{"name": "MIT", "state": "MA", "type": "private"}'
```

#### GET /universities/{id}
Get university details including assigned courses.

**Path Parameters:**
- `id` (integer) - University ID

**Response:**
```json
{
  "id": 1,
  "name": "UFRJ",
  "state": "RJ", 
  "type": "public",
  "courses": [
    {
      "id": 1,
      "name": "Ciência da computação"
    },
    {
      "id": 2,
      "name": "Biologia"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/universities/1
```

#### PUT /universities/{id}
Update university details.

**Path Parameters:**
- `id` (integer) - University ID

**Request Body:**
```json
{
  "name": "string",
  "state": "string",
  "type": "public" | "private" 
}
```

**Response:**
```json
{
  "message": "University updated successfully"
}
```

**Example:**
```bash
curl -X PUT http://localhost:8000/universities/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "UFRJ - Updated", "state": "RJ", "type": "public"}'
```

#### DELETE /universities/{id}
Delete a university.

**Path Parameters:**
- `id` (integer) - University ID

**Response:**
```json
{
  "message": "University deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/universities/1
```

#### PUT /universities/{id}/courses
Assign courses to a university.

**Path Parameters:**
- `id` (integer) - University ID

**Request Body:**
```json
{
  "courses": [1, 2, 3]
}
```

**Response:**
```json
{
  "message": "Courses assigned successfully"
}
```

**Example:**
```bash
curl -X PUT http://localhost:8000/universities/1/courses \
  -H "Content-Type: application/json" \
  -d '{"courses": [1, 3, 5]}'
```

---

## Data Models

### University
```json
{
  "id": "integer (auto-generated)",
  "name": "string (required)", 
  "state": "string (required)",
  "type": "public | private (required)",
  "courses": "array of Course objects (read-only)"
}
```

### Course  
```json
{
  "id": "integer",
  "name": "string"
}
```

### Available Courses
The system includes these predefined courses:

| ID | Name |
|----|------|
| 1 | Ciência da computação |
| 2 | Biologia |  
| 3 | História |
| 4 | Direito |
| 5 | Medicina |

---

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

---

## Error Responses

All errors return a JSON object with error details:

```json
{
  "detail": "Error message description"
}
```

**Examples:**

**404 Not Found:**
```json
{
  "detail": "University not found"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "type"],
      "msg": "value is not a valid enumeration member; permitted: 'public', 'private'",
      "type": "type_error.enum"
    }
  ]
}
```

---

## Complete Example Workflow

Here's a complete example showing typical API usage:

```bash
# 1. Check API health
curl http://localhost:8000/health

# 2. Get all universities
curl http://localhost:8000/universities

# 3. Create a new university
NEW_UNIV=$(curl -X POST http://localhost:8000/universities \
  -H "Content-Type: application/json" \
  -d '{"name": "Stanford", "state": "CA", "type": "private"}')

# Extract the ID (assuming jq is available)
UNIV_ID=$(echo $NEW_UNIV | jq '.id')

# 4. Get the created university
curl http://localhost:8000/universities/$UNIV_ID

# 5. Assign courses to the university
curl -X PUT http://localhost:8000/universities/$UNIV_ID/courses \
  -H "Content-Type: application/json" \
  -d '{"courses": [1, 2, 5]}'

# 6. Get university with courses
curl http://localhost:8000/universities/$UNIV_ID

# 7. Update university details
curl -X PUT http://localhost:8000/universities/$UNIV_ID \
  -H "Content-Type: application/json" \
  -d '{"name": "Stanford University", "state": "CA", "type": "private"}'

# 8. Delete the university
curl -X DELETE http://localhost:8000/universities/$UNIV_ID
```

---

## Interactive API Documentation

When the server is running, you can access interactive API documentation at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

These provide a web interface to explore and test the API endpoints.

---

## Distributed Usage

For distributed communication between two computers:

**Computer 1 (Server):**
```bash
# Start the API server
./scripts/start_coordinator.sh
```

**Computer 2 (Client):**
```bash
# Update IP in client_demo.sh, then run
./scripts/client_demo.sh
```

The client demo script shows all API endpoints working across the network between two computers.
