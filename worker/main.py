"""
Simple Worker Node

A minimal FastAPI worker for testing distributed connectivity.
Optional component - the main pattern is client-server communication.
"""

from fastapi import FastAPI
import uuid
import time

app = FastAPI(
    title="Simple Worker Node", 
    description="Simple Worker for Distributed System Demo",
    version="1.0.0"
)

WORKER_ID = f"worker-{str(uuid.uuid4())[:8]}"

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
