#!/bin/bash

echo "Starting Coordinator (Computer 1)..."

# Activate virtual environment
source .venv/bin/activate

# Start coordinator
echo "Starting coordinator on port 8000..."
cd coordinator
python main.py
