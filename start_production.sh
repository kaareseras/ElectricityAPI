#!/bin/bash
"""
Production startup script with optimized settings.
Use this for production deployment.
"""

echo "Starting FastAPI application in production mode..."

# Set production environment variables
export RUNNING_IN_PRODUCTION=True
export DEBUG=False

# Start gunicorn with optimized settings
exec gunicorn \
    --config src/gunicorn.conf.py \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class src.my_uvicorn_worker.MyUvicornWorker \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --timeout 120 \
    --graceful-timeout 30 \
    --keepalive 5 \
    --preload \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    src.fastapi_app.app:app
