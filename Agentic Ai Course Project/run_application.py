import uvicorn
import os
import sys

# Ensure backend directory is in python search path
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    print("=" * 70)
    print(" RESEARCH GRANT MANAGEMENT SYSTEM -- MULTI-AGENT AGENTIC AI")
    print(" Host Institution: KLE Technological University, Hubballi")
    print("=" * 70)
    print(" Server URL: http://127.0.0.1:8000")
    print(" API Documentation: http://127.0.0.1:8000/docs")
    print(" Teacher Dashboard: http://127.0.0.1:8000 (Switch to Teacher View)")
    print("=" * 70)
    
    # Run uvicorn server serving both API and bundled React frontend
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False, app_dir=backend_dir)
