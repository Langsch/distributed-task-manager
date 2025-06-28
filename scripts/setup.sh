#!/bin/bash

# setup.sh - Setup script for the distributed university management system

echo "🎓 Setting up Distributed University Management System"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update the coordinator IP in worker/main.py (line 18)"
echo "2. Run './scripts/start_coordinator.sh' on Computer 1"
echo "3. Run './scripts/start_worker.sh' on Computer 2"
echo ""
echo "API Documentation will be available at:"
echo "- Coordinator: http://localhost:8000/docs"
echo "- Worker: http://localhost:8001/docs"
