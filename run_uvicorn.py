#!/usr/bin/env python3
"""
Clean replacement for: python3 -m uvicorn src.fastapi_app.app:app --reload --port=8000
This script properly handles Ctrl+C and ensures the port is freed.
"""

import os
import signal
import subprocess
import sys
import time


def kill_port_8000():
    """Kill any processes using port 8000"""
    try:
        # Find processes using port 8000
        result = subprocess.run(["lsof", "-ti:8000"], capture_output=True, text=True)

        if result.stdout.strip():
            pids = result.stdout.strip().split("\n")
            print(f"🧹 Cleaning up processes on port 8000: {', '.join(pids)}")

            for pid in pids:
                try:
                    subprocess.run(["kill", "-TERM", pid], check=False)
                except Exception:
                    pass

            # Wait a bit, then force kill if needed
            time.sleep(1)

            # Check again and force kill if still there
            result = subprocess.run(["lsof", "-ti:8000"], capture_output=True, text=True)

            if result.stdout.strip():
                pids = result.stdout.strip().split("\n")
                for pid in pids:
                    try:
                        subprocess.run(["kill", "-KILL", pid], check=False)
                    except Exception:
                        pass

    except FileNotFoundError:
        # lsof not available, try alternative
        subprocess.run(["pkill", "-f", "uvicorn.*8000"], check=False)


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Stopping uvicorn...")
    kill_port_8000()
    print("✅ Port 8000 should be free now")
    sys.exit(0)


def main():
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Set environment variables
    os.environ["DEBUG"] = "True"
    os.environ["RUNNING_IN_PRODUCTION"] = "False"

    print("🚀 Starting uvicorn (Press Ctrl+C to stop)")

    try:
        # Run your exact command
        result = subprocess.run(
            ["python3", "-m", "uvicorn", "src.fastapi_app.app:app", "--reload", "--port=8000"], check=False
        )

        print(f"✅ Uvicorn exited with code {result.returncode}")

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        kill_port_8000()
        print("✅ Port 8000 cleaned up")
    except Exception as e:
        print(f"❌ Error: {e}")
        kill_port_8000()
        sys.exit(1)
    finally:
        # Ensure port is clean on any exit
        kill_port_8000()


if __name__ == "__main__":
    main()
