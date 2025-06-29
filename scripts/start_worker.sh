#!/bin/bash

echo "Starting Worker (Computer 2)..."

# Activate virtual environment  
source .venv/bin/activate

# Start worker
echo "Starting worker on port 8001..."
cd worker
python main.py
