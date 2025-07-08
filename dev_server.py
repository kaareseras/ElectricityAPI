#!/usr/bin/env python3
"""
Development server with proper shutdown handling.
"""

import os
import signal
import sys

import uvicorn


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n🛑 Received shutdown signal. Stopping server...")
    sys.exit(0)


if __name__ == "__main__":
    # Set up signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

    # Set development environment variables
    os.environ.setdefault("DEBUG", "True")
    os.environ.setdefault("RUNNING_IN_PRODUCTION", "False")

    print("🚀 Starting FastAPI development server...")
    print("📝 Press Ctrl+C to stop the server")

    try:
        # Your exact command but with optimizations
        uvicorn.run(
            "src.fastapi_app.app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_excludes=[
                "*.db",
                "*.sqlite",
                "*.log",
                "__pycache__/*",
                "*.pyc",
                ".git/*",
                "node_modules/*",
                ".venv/*",
            ],
            log_level="info",
            access_log=True,
            use_colors=True,
            # Optimize for development
            reload_delay=0.25,  # Faster reload detection
            timeout_keep_alive=5,
        )
    except KeyboardInterrupt:
        print("\n✅ Server stopped successfully!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)
