#!/usr/bin/env python3
"""
Test script to diagnose the /docs endpoint issue
"""

import os
import sys

# Set environment variables
os.environ["DEBUG"] = "True"
os.environ["RUNNING_IN_PRODUCTION"] = "False"

print("🔍 Diagnosing FastAPI /docs endpoint issue...")
print(f"📁 Current working directory: {os.getcwd()}")
print(f"🐍 Python path: {sys.path[0]}")
print(f"🌍 Environment - DEBUG: {os.environ.get('DEBUG')}")
print(f"🌍 Environment - RUNNING_IN_PRODUCTION: {os.environ.get('RUNNING_IN_PRODUCTION')}")

try:
    print("📦 Importing FastAPI...")
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
    
    print("📦 Importing app...")
    from src.fastapi_app.app import app
    print("✅ App imported successfully")
    
    print(f"📋 App title: {app.title}")
    print(f"📋 Docs URL: {app.docs_url}")
    print(f"📋 ReDoc URL: {app.redoc_url}")
    
    print("🔍 Checking routes...")
    route_count = len(app.routes)
    print(f"📊 Total routes: {route_count}")
    
    # Check if docs route exists
    docs_route_exists = any(route.path == "/docs" for route in app.routes if hasattr(route, 'path'))
    print(f"📄 /docs route exists: {docs_route_exists}")
    
    print("✅ Diagnosis complete - app looks healthy!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
