#!/bin/bash

# start_worker.sh - Start the worker service (Computer 2)

echo "🎓 Starting University Management Worker (Computer 2)"
echo "====================================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Get local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "📍 Worker IP Address: $LOCAL_IP"

# Check if coordinator URL is configured
cd worker
COORDINATOR_URL=$(grep "COORDINATOR_URL" main.py | cut -d'"' -f2)
echo "🔗 Configured coordinator: $COORDINATOR_URL"

if [[ "$COORDINATOR_URL" == "http://192.168.1.100:8000" ]]; then
    echo "⚠️  WARNING: Please update COORDINATOR_URL in worker/main.py with the actual coordinator IP"
    echo "   Current: $COORDINATOR_URL"
    echo "   Should be something like: http://[COORDINATOR_IP]:8000"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🚀 Starting worker service on port 8001..."
echo "📖 API Documentation: http://localhost:8001/docs"
echo "❤️  Health Check: http://localhost:8001/health"
echo ""
echo "Press Ctrl+C to stop the service"

# Start the FastAPI application
python main.py
