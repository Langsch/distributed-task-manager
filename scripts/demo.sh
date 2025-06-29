#!/bin/bash

echo "=== University Management API Demo ==="

COORDINATOR_URL="http://localhost:8000"

# Check if coordinator is running
echo "Checking if coordinator is running..."
if ! curl -s $COORDINATOR_URL/health > /dev/null; then
    echo "❌ Coordinator not found. Please start it first: ./scripts/start_coordinator.sh"
    exit 1
fi
echo "✅ Coordinator is running"

echo ""
echo "🚀 Demo: Testing the University Management API"

# 1. Check coordinator health
echo ""
echo "1. Coordinator health check:"
curl -s $COORDINATOR_URL/health | python3 -m json.tool

# 2. Get universities
echo ""
echo "2. Getting all universities:"
curl -s $COORDINATOR_URL/universities | python3 -m json.tool

# 3. Create a new university
echo ""
echo "3. Creating a new university (UFF):"
NEW_UNIVERSITY=$(curl -s -X POST "$COORDINATOR_URL/universities" \
     -H "Content-Type: application/json" \
     -d '{"name": "UFF", "state": "RJ", "type": "public"}')
echo $NEW_UNIVERSITY | python3 -m json.tool

# Extract the new university ID
NEW_ID=$(echo $NEW_UNIVERSITY | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

# 4. Get university details
echo ""
echo "4. Getting university details (ID: $NEW_ID):"
curl -s $COORDINATOR_URL/universities/$NEW_ID | python3 -m json.tool

# 5. Assign courses to university
echo ""
echo "5. Assigning courses to university (courses 1 and 2):"
curl -s -X PUT "$COORDINATOR_URL/universities/$NEW_ID/courses" \
     -H "Content-Type: application/json" \
     -d '{"courses": [1, 2]}' | python3 -m json.tool

# 6. Get university details with courses
echo ""
echo "6. Getting university details with courses:"
curl -s $COORDINATOR_URL/universities/$NEW_ID | python3 -m json.tool

# 7. Update university
echo ""
echo "7. Updating university details:"
curl -s -X PUT "$COORDINATOR_URL/universities/$NEW_ID" \
     -H "Content-Type: application/json" \
     -d '{"name": "UFF - Universidade Federal Fluminense", "state": "RJ", "type": "public"}' | python3 -m json.tool

# 8. Get updated university details
echo ""
echo "8. Getting updated university details:"
curl -s $COORDINATOR_URL/universities/$NEW_ID | python3 -m json.tool

# 9. Delete university
echo ""
echo "9. Deleting university:"
curl -s -X DELETE "$COORDINATOR_URL/universities/$NEW_ID" | python3 -m json.tool

# 10. Verify deletion
echo ""
echo "10. Verifying deletion (should return 404):"
curl -s -w "%{http_code}" $COORDINATOR_URL/universities/$NEW_ID | python3 -m json.tool 2>/dev/null || echo "404 - University not found (expected)"

echo ""
echo "✅ Demo complete!"
echo ""
echo "🌐 For distributed testing:"
echo "  - Run this on Computer 1: ./scripts/start_coordinator.sh"
echo "  - Run this on Computer 2: ./scripts/client_demo.sh (after updating IP)"
