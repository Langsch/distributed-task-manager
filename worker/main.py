"""
Simple Worker Node

A minimal FastAPI worker that can be used for testing distributed connectivity.
This worker provides basic health check functionality and can demonstrate
that another computer is reachable on the network.

In the simple distributed model, this worker is optional - the main pattern
is for Computer 2 to act as a client making requests to Computer 1's API.

Endpoints:
- GET /health - Health check with worker ID and uptime

Usage:
    python main.py
    # or  
    uvicorn main:app --host 0.0.0.0 --port 8001
"""

from fastapi import FastAPI
import uuid
import time

app = FastAPI(
    title="Simple Worker Node", 
    description="Simple Worker for Distributed System Demo",
    version="1.0.0"
)

# Worker configuration
WORKER_ID = f"worker-{str(uuid.uuid4())[:8]}"

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "worker_id": WORKER_ID,
        "uptime": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    print(f"Starting simple worker {WORKER_ID}")
    uvicorn.run(app, host="0.0.0.0", port=8001)
