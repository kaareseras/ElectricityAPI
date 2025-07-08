#!/bin/bash
# Direct replacement for: python3 -m uvicorn src.fastapi_app.app:app --reload --port=8000
# This handles Ctrl+C properly and returns to prompt

echo "🚀 Starting uvicorn (Ctrl+C to stop)..."

# Set environment for better performance
export DEBUG=True
export RUNNING_IN_PRODUCTION=False

# Function to handle cleanup
cleanup() {
    echo ""
    echo "🛑 Stopping uvicorn..."
    
    # Kill the uvicorn process if it's still running
    if [ ! -z "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        echo "📝 Sending SIGTERM to process $PID..."
        kill -TERM "$PID" 2>/dev/null
        
        # Wait a bit for graceful shutdown
        sleep 2
        
        # Force kill if still running
        if kill -0 "$PID" 2>/dev/null; then
            echo "🔥 Force killing process $PID..."
            kill -KILL "$PID" 2>/dev/null
        fi
    fi
    
    # Also kill any remaining uvicorn processes on port 8000
    echo "🧹 Cleaning up any remaining processes on port 8000..."
    pkill -f "uvicorn.*8000" 2>/dev/null || true
    
    echo "✅ Uvicorn stopped. Port 8000 should be free now."
    exit 0
}

# Trap signals for clean exit
trap cleanup SIGINT SIGTERM EXIT

# Run your exact command in background
python3 -m uvicorn src.fastapi_app.app:app --reload --port=8000 &

# Store the process ID
PID=$!
echo "📋 Uvicorn PID: $PID"

# Wait for the background process
wait $PID

# Normal exit
echo "✅ Uvicorn exited normally."
