#!/usr/bin/env python3
"""
Simple script to run the HTTP Data Serve API server.
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting HTTP Data Serve API...")
    print("📍 Server will be available at:")
    print("   - Web UI: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - API: http://localhost:8000/api/data")
    print("\n✨ Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
