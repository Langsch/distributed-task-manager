#!/bin/bash

# start_coordinator.sh - Start the coordinator service (Computer 1)

echo "🎓 Starting University Management Coordinator (Computer 1)"
echo "========================================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Get local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "📍 Local IP Address: $LOCAL_IP"
echo "🌐 The worker should use: http://$LOCAL_IP:8000"

# Change to coordinator directory
cd coordinator

echo "🚀 Starting coordinator service on port 8000..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/"
echo ""
echo "Press Ctrl+C to stop the service"

# Start the FastAPI application
python main.py
