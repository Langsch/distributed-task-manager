#!/bin/bash

# get_ip.sh - Helper script to find your IP address

echo "🔍 Your Computer's IP Addresses:"
echo "================================"

# Try different methods to get IP
if command -v hostname &> /dev/null; then
    IPS=$(hostname -I 2>/dev/null)
    if [ ! -z "$IPS" ]; then
        echo "📍 All IPs: $IPS"
    fi
fi

# Get specific network interfaces
echo ""
echo "🌐 Network Interfaces:"
if command -v ip &> /dev/null; then
    ip addr show | grep "inet " | grep -v "127.0.0.1" | while read line; do
        INTERFACE=$(echo $line | awk '{print $NF}')
        IP=$(echo $line | awk '{print $2}' | cut -d'/' -f1)
        echo "  $INTERFACE: $IP"
    done
elif command -v ifconfig &> /dev/null; then
    ifconfig | grep -A1 "^[a-z]" | grep "inet " | grep -v "127.0.0.1" | while read line; do
        IP=$(echo $line | awk '{print $2}')
        echo "  $IP"
    done
fi

echo ""
echo "💡 To update config.py:"
echo "   Edit the COORDINATOR_IP line with the IP both computers can access"
echo ""
echo "🧪 Test connectivity from Computer 2:"
echo "   ping -c 3 [IP_ADDRESS]"
