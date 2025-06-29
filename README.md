# Distributed University Management System

A clean, simple distributed system built with FastAPI that demonstrates REST API communication between two computers.

## Overview

This project shows how to connect two computers through a distributed REST API:
- **Computer 1 (Server)**: Runs the university management API using FastAPI
- **Computer 2 (Client)**: Makes HTTP requests to Computer 1's API server

## Features

- ✅ Complete university management (CRUD operations)
- ✅ Course assignment to universities  
- ✅ Clean RESTful API design
- ✅ SQLite database backend
- ✅ True distributed client-server communication
- ✅ Easy setup and demonstration

## Quick Start

### Setup (Both Computers)
```bash
# Clone and setup
git clone <repository>
cd distributed-task-manager
./scripts/setup.sh
```

### Running the System

**Computer 1 (Server):**
```bash
./scripts/start_coordinator.sh
```

**Computer 2 (Client):**
```bash
# First, update the IP address in scripts/client_demo.sh
# Then run the client demo
./scripts/client_demo.sh
```

### Testing Locally
```bash
./scripts/demo.sh
```

## API Endpoints

### Universities
- `GET /universities` - List all universities
- `POST /universities` - Create a new university  
- `GET /universities/{id}` - Get university details with courses
- `PUT /universities/{id}` - Update university details
- `DELETE /universities/{id}` - Delete university
- `PUT /universities/{id}/courses` - Assign courses to university

### System
- `GET /health` - Health check

See [API.md](API.md) for detailed documentation with examples.

## Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Computer 1    │ ◄──────────────► │   Computer 2    │
│   (Server)      │                  │    (Client)     │
│   Port 8000     │                  │   curl/HTTP     │
│                 │                  │   requests      │
└─────────────────┘                  └─────────────────┘
```

## Configuration

Update IP addresses in:
- `scripts/client_demo.sh` (line 6) - Set Computer 1's IP address
- `config.py` - Network configuration

## Project Structure

```
distributed-task-manager/
├── coordinator/
│   ├── main.py          # Main FastAPI application
│   ├── database.py      # SQLite database setup
│   └── __init__.py      
├── scripts/
│   ├── setup.sh         # Initial setup
│   ├── start_coordinator.sh  # Start server
│   ├── client_demo.sh   # Client demonstration (Computer 2)
│   ├── demo.sh          # Local testing
├── README.md            # This file
├── API.md               # API documentation
├── config.py            # Configuration
├── requirements.txt     # Python dependencies
└── .gitignore          # Git ignore rules
```

## Technology Stack

- **Python 3.8+**
- **FastAPI** - REST API framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database
- **uvicorn** - ASGI server

## Sample Data

The system comes with sample universities and courses:

**Universities:**
- UFRJ (RJ, public)
- PUC-Rio (RJ, private)  
- USP (SP, public)
- Unicamp (SP, public)

**Courses:**
- Ciência da computação
- Biologia
- História
- Direito
- Medicina

## Distributed Setup Guide

For step-by-step setup instructions, run:
```bash
./scripts/distributed_setup_guide.sh
```

## What This Demonstrates

- ✅ **Simple Architecture**: Clean client-server model without unnecessary complexity
- ✅ **Network Communication**: Computer 2 making HTTP requests to Computer 1
- ✅ **Real Distribution**: Two separate computers communicating over the network
- ✅ **RESTful Design**: Proper HTTP methods and status codes
- ✅ **Data Persistence**: SQLite database maintains state across requests
- ✅ **Easy to Understand**: Minimal codebase focused on core concepts

## Troubleshooting

**Connection Issues:**
- Ensure both computers are on the same network
- Check firewall settings on Computer 1
- Verify Computer 1's IP address is correct
- Make sure Computer 1 is running the server

**Common Commands:**
```bash
# Check if server is running
curl http://COMPUTER1_IP:8000/health

# Test network connectivity
ping COMPUTER1_IP

# View server logs
# Check terminal where start_coordinator.sh is running
```

This is a perfect example of a clean, well-documented distributed system! 🚀
