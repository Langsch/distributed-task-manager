# Configuration file for the distributed university management system

# Coordinator Configuration (Computer 1)
COORDINATOR_HOST = "0.0.0.0"
COORDINATOR_PORT = 8000

# Worker Configuration (Computer 2)
WORKER_HOST = "0.0.0.0"  
WORKER_PORT = 8001

# Network Configuration
# UPDATE THIS: Replace with Computer 1's actual IP address
COORDINATOR_IP = "192.168.0.98"

# Database Configuration
DATABASE_NAME = "university.sqlite"

# System Configuration
MAX_WORKERS = 5
HEALTH_CHECK_INTERVAL = 30  # seconds
REQUEST_TIMEOUT = 10  # seconds
