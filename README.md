# Distributed University Management System

I built this distributed system to show how two computers can communicate through a REST API. It's a straightforward FastAPI application that manages university data across a network.

## What it does

This connects two computers in a simple client-server setup:
- **Computer 1** runs the university management API server
- **Computer 2** makes HTTP requests to manage university data remotely

## Features

- University management (create, read, update, delete)
- Course assignment system
- RESTful API design
- SQLite database storage

## Setup Instructions

### Computer 1 (Server Setup)

**Step 1: Clone and Setup**
```bash
git clone https://github.com/Langsch/distributed-task-manager.git
cd distributed-task-manager
./scripts/setup.sh
```

**Step 2: Find Your IP Address**
```bash
# Find your network IP address
ip addr show | grep inet | grep -v 127.0.0.1
# or
hostname -I
```
Write down the IP address (like 192.168.1.100) - you'll need this for Computer 2.

**Step 3: Configure Firewall (if needed)**
```bash
# Allow port 8000 through firewall
sudo ufw allow 8000
# or for specific networks
sudo ufw allow from 192.168.1.0/24 to any port 8000
```

**Step 4: Start the Server**
```bash
./scripts/start_coordinator.sh
```
Keep this terminal open - the server logs will appear here.

**Step 5: Test Server is Running**
```bash
# In a new terminal, test locally
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### Computer 2 (Client Setup)

**Step 1: Clone and Setup**
```bash
git clone https://github.com/Langsch/distributed-task-manager.git
cd distributed-task-manager
./scripts/setup.sh
```

**Step 2: Configure Client**
Edit the client demo script with Computer 1's IP address:
```bash
nano scripts/client_demo.sh
# Change line 6: SERVER_IP="localhost" 
# To: SERVER_IP="192.168.1.100"  # Use Computer 1's actual IP
```

**Step 3: Test Connection**
```bash
# Test if you can reach Computer 1
ping 192.168.1.100  # Use Computer 1's IP
curl http://192.168.1.100:8000/health
```

**Step 4: Run Client Demo**
```bash
./scripts/client_demo.sh
```
This demonstrates all API operations from Computer 2 to Computer 1.

### Local Testing (Single Computer)
To test everything on one computer first:
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


## Distributed Setup Guide

For step-by-step setup instructions, run:
```bash
./scripts/distributed_setup_guide.sh
```

## What This Demonstrates

- **Simple Architecture**: Clean client-server model without unnecessary complexity
- **Network Communication**: Computer 2 making HTTP requests to Computer 1
- **Real Distribution**: Two separate computers communicating over the network
- **RESTful Design**: Proper HTTP methods and status codes
- **Data Persistence**: SQLite database maintains state across requests
- **Easy to Understand**: Minimal codebase focused on core concepts

## Testing & Verification

### Step-by-Step Testing Process

**1. Verify Computer 1 Server is Running**
```bash
# On Computer 1
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

**2. Test Network Connectivity**
```bash
# On Computer 2
ping COMPUTER1_IP
# Should show successful ping responses
```

**3. Test Remote API Access**
```bash
# On Computer 2
curl http://COMPUTER1_IP:8000/health
# Expected: {"status":"healthy"}
```

**4. Test Full API Operations**
```bash
# On Computer 2
./scripts/client_demo.sh
# This runs a complete test of all API endpoints
```

### Troubleshooting

**Connection Issues:**
- Make sure both computers are on the same network
- Check firewall settings on Computer 1 (allow port 8000)
- Verify Computer 1's IP address is correct in client_demo.sh
- Make sure Computer 1 server is running (check terminal output)

**Network Testing Commands:**
```bash
# Test basic connectivity
ping COMPUTER1_IP

# Test if port 8000 is reachable
telnet COMPUTER1_IP 8000
# or
nc -zv COMPUTER1_IP 8000

# Test API health endpoint
curl -v http://COMPUTER1_IP:8000/health

# Check server logs on Computer 1
# Look at the terminal where start_coordinator.sh is running
```

**Common Issues:**
- **Firewall blocking**: Run `sudo ufw allow 8000` on Computer 1
- **Wrong IP address**: Double-check with `hostname -I` on Computer 1
- **Network isolation**: Make sure both computers are on same subnet
- **Server not started**: Verify start_coordinator.sh is running and showing "Uvicorn running"

