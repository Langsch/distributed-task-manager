#!/bin/bash

# demo.sh - Demo script for testing the distributed system

echo "🎓 University Management System Demo"
echo "==================================="

# Check if services are running
echo "🔍 Checking if services are running..."

# Check coordinator
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Coordinator is running on port 8000"
else
    echo "❌ Coordinator not found on port 8000"
    echo "   Please start coordinator first: ./scripts/start_coordinator.sh"
    exit 1
fi

# Check worker
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ Worker is running on port 8001"
else
    echo "❌ Worker not found on port 8001"
    echo "   Please start worker first: ./scripts/start_worker.sh"
    exit 1
fi

echo ""
echo "🚀 Running demo scenarios..."

# 1. Check system status
echo "📊 1. System Status:"
curl -s http://localhost:8000/ | python3 -m json.tool

echo ""
echo "👥 2. Registered Workers:"
curl -s http://localhost:8000/workers | python3 -m json.tool

echo ""
echo "🏫 3. Available Universities:"
curl -s http://localhost:8000/universities | python3 -m json.tool

echo ""
echo "📚 4. Available Courses:"
curl -s http://localhost:8000/courses | python3 -m json.tool

echo ""
echo "👨‍🎓 5. Creating a new student (distributed processing):"
curl -X POST "http://localhost:8000/students" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Maria Santos",
       "email": "maria.santos@example.com",
       "university_id": 1,
       "course_id": 1,
       "enrollment_year": 2024
     }' | python3 -m json.tool

echo ""
echo "📈 6. Worker Statistics:"
curl -s http://localhost:8001/stats | python3 -m json.tool

echo ""
echo "🔄 7. Testing Worker Analytics:"
curl -X POST "http://localhost:8001/test/analytics" \
     -H "Content-Type: application/json" | python3 -m json.tool

echo ""
echo "✅ Demo complete!"
echo ""
echo "💡 Next steps:"
echo "   - Visit http://localhost:8000/docs for coordinator API"
echo "   - Visit http://localhost:8001/docs for worker API"
echo "   - Create more students, universities, and courses"
echo "   - Monitor statistics at /stats endpoints"
