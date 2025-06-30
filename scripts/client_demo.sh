#!/bin/bash

echo "=== Distributed University Management Client Demo ==="
echo "Running on Computer 2 - Making requests to Computer 1"
echo ""

COORDINATOR_IP="${COORDINATOR_IP:-192.168.1.100}"
COORDINATOR_URL="http://${COORDINATOR_IP}:8000"

echo "Target: Computer 1 at $COORDINATOR_URL"
echo ""

echo "1. Testing connection to Computer 1..."
if ! curl -s --connect-timeout 5 $COORDINATOR_URL/health > /dev/null; then
    echo "Cannot reach Computer 1. Please check:"
    echo "   - Computer 1 is running: ./scripts/start_coordinator.sh"
    echo "   - IP address is correct: $COORDINATOR_IP"
    echo "   - Network connectivity and firewall settings"
    exit 1
fi
echo "Successfully connected to Computer 1!"

echo ""
echo "Demo: Computer 2 making requests to Computer 1's API"

# 2. Get coordinator health
echo ""
echo "2. Getting Computer 1 health status:"
curl -s $COORDINATOR_URL/health | python3 -m json.tool

# 3. Get all universities from Computer 1
echo ""
echo "3. Getting universities from Computer 1:"
curl -s $COORDINATOR_URL/universities | python3 -m json.tool

# 4. Create a new university on Computer 1
echo ""
echo "4. Creating a new university on Computer 1:"
NEW_UNIVERSITY=$(curl -s -X POST "$COORDINATOR_URL/universities" \
     -H "Content-Type: application/json" \
     -d '{"name": "Remote University", "state": "RS", "type": "public"}')
echo $NEW_UNIVERSITY | python3 -m json.tool

# Extract the new university ID
NEW_ID=$(echo $NEW_UNIVERSITY | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

# 5. Get the created university details
echo ""
echo "5. Getting university details from Computer 1 (ID: $NEW_ID):"
curl -s $COORDINATOR_URL/universities/$NEW_ID | python3 -m json.tool

# 6. Update the university on Computer 1
echo ""
echo "6. Updating university on Computer 1:"
curl -s -X PUT "$COORDINATOR_URL/universities/$NEW_ID" \
     -H "Content-Type: application/json" \
     -d '{"name": "Remote University - Updated from Computer 2", "state": "RS", "type": "private"}' | python3 -m json.tool

# 7. Get updated university details
echo ""
echo "7. Getting updated university details:"
curl -s $COORDINATOR_URL/universities/$NEW_ID | python3 -m json.tool

# 8. Assign courses to the university
echo ""
echo "8. Assigning courses to university on Computer 1:"
curl -s -X PUT "$COORDINATOR_URL/universities/$NEW_ID/courses" \
     -H "Content-Type: application/json" \
     -d '{"courses": [1, 3]}' | python3 -m json.tool

# 9. Get university with assigned courses
echo ""
echo "9. Getting university with courses:"
curl -s $COORDINATOR_URL/universities/$NEW_ID | python3 -m json.tool

# 10. Delete the university
echo ""
echo "10. Deleting university on Computer 1:"
curl -s -X DELETE "$COORDINATOR_URL/universities/$NEW_ID" | python3 -m json.tool

# 11. Final verification
echo ""
echo "11. Final universities list:"
curl -s $COORDINATOR_URL/universities | python3 -m json.tool

echo ""
echo "Distributed demo complete!"
echo ""
echo "Summary:"
echo "  - Computer 2 successfully connected to Computer 1"
echo "  - Performed CRUD operations on Computer 1 from Computer 2"
echo "  - University created, updated, and deleted remotely"
echo "  - Demonstrates distributed REST API communication"
echo ""
echo "This shows Computer 2 acting as a client to Computer 1's API server"
