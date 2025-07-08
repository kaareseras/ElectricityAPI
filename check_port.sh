#!/bin/bash
# Script to check and free port 8000

echo "🔍 Checking what's using port 8000..."

# Check if port 8000 is in use
PORT_USED=$(lsof -ti:8000 2>/dev/null)

if [ -z "$PORT_USED" ]; then
    echo "✅ Port 8000 is free!"
else
    echo "🚫 Port 8000 is being used by process(es): $PORT_USED"
    echo "📋 Process details:"
    lsof -i:8000 2>/dev/null || echo "Could not get process details"
    
    echo ""
    read -p "Do you want to kill these processes? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🔥 Killing processes using port 8000..."
        kill -TERM $PORT_USED 2>/dev/null || true
        sleep 2
        
        # Check if still running and force kill
        STILL_RUNNING=$(lsof -ti:8000 2>/dev/null)
        if [ ! -z "$STILL_RUNNING" ]; then
            echo "🔥 Force killing remaining processes..."
            kill -KILL $STILL_RUNNING 2>/dev/null || true
        fi
        
        # Final check
        FINAL_CHECK=$(lsof -ti:8000 2>/dev/null)
        if [ -z "$FINAL_CHECK" ]; then
            echo "✅ Port 8000 is now free!"
        else
            echo "❌ Some processes are still using port 8000"
        fi
    else
        echo "👍 Processes left running"
    fi
fi
