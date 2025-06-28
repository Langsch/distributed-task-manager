# Getting Started Guide

## Quick Setup (5 Minutes)

### Step 1: Setup Both Computers
```bash
# Clone/copy this project to both computers
./scripts/setup.sh
```

### Step 2: Configure Network
Edit `config.py` and update the coordinator IP:
```python
COORDINATOR_IP = "192.168.1.XXX"  # Replace with Computer 1's IP
```

### Step 3: Start Services

**Computer 1 (Coordinator):**
```bash
./scripts/start_coordinator.sh
```

**Computer 2 (Worker):**
```bash
./scripts/start_worker.sh
```

### Step 4: Test Everything
```bash
./scripts/demo.sh
```

## What You'll See

1. **Automatic Registration**: Worker registers with coordinator
2. **Distributed Processing**: Student creation delegated to worker
3. **API Documentation**: Available at `:8000/docs` and `:8001/docs`
4. **Real-time Statistics**: Monitor system performance

## For Your Professor Demo

### Show These Features:
1. **Service Discovery**: Worker auto-registers
2. **Load Balancing**: Tasks distributed to workers
3. **REST API**: All HTTP methods working
4. **Fault Tolerance**: System works even if worker fails
5. **Monitoring**: Health checks and statistics

### API Examples:
```bash
# Create University
curl -X POST "http://localhost:8000/universities" \
     -H "Content-Type: application/json" \
     -d '{"name": "MIT", "state": "MA", "type": "private"}'

# Create Student (distributed)
curl -X POST "http://localhost:8000/students" \
     -H "Content-Type: application/json" \
     -d '{"name": "João Silva", "email": "joao@test.com", "university_id": 1, "course_id": 1, "enrollment_year": 2024}'

# Check Statistics
curl http://localhost:8000/stats
curl http://localhost:8001/stats
```

## Troubleshooting

**Worker not registering?**
- Check IP address in `config.py`
- Ensure both computers on same network
- Check firewall settings

**Dependencies failing?**
- Try: `pip install --upgrade pip`
- Use Python 3.8-3.12 (avoid 3.13)

**Need help?**
- Check logs in terminal
- Visit `/docs` endpoints for API documentation
- Use `./scripts/demo.sh` for testing
