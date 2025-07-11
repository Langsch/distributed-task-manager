#!/bin/bash

echo "=== Distributed University Management System - Setup ==="

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To start the system:"
echo "1. Run server: ./scripts/start_coordinator.sh"
echo "2. Test locally: ./scripts/demo.sh"
echo "3. For distributed testing: ./scripts/client_demo.sh (update IP first)"
