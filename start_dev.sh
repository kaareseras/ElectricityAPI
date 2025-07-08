#!/bin/bash
# Optimized version of your uvicorn command with proper shutdown handling

echo "🚀 Starting FastAPI with optimized uvicorn settings..."
echo "📝 Press Ctrl+C to stop the server"

# Set development environment for faster startup
export DEBUG=True
export RUNNING_IN_PRODUCTION=False

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo "✅ Server stopped successfully!"
    exit 0
}

# Set up signal traps for clean shutdown
trap cleanup SIGINT SIGTERM

# Your exact command with optimizations
python3 -m uvicorn src.fastapi_app.app:app \
    --reload \
    --port=8000 \
    --host=0.0.0.0 \
    --reload-delay=0.25 \
    --timeout-keep-alive=5 \
    --log-level=info \
    --use-colors \
    --reload-exclude="*.db" \
    --reload-exclude="*.sqlite" \
    --reload-exclude="*.log" \
    --reload-exclude="__pycache__" \
    --reload-exclude=".git" || cleanup
