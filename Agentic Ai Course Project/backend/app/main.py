from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi import Request
import uuid
import traceback
import os
from .config import settings
from .database import engine, Base
from .seed_data import seed_database
from .core.llm import llm_service
from .api.routes_projects import router as projects_router
from .api.routes_agents import router as agents_router
from .api.routes_labs import router as labs_router
from .api.routes_teacher import router as teacher_router
from .api.routes_researcher import router as researcher_router

# Ensure DB tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multi-Agent Agentic AI Application for End-to-End Research Grant Management (KLE Technological University)"
)

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    req_id = str(uuid.uuid4())[:8]
    print(f"[UNHANDLED EXCEPTION {req_id}] {request.method} {request.url}: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "error_status": "INTERNAL_SERVER_ERROR",
            "message": str(exc) or "Internal server error during agent execution",
            "failed_operation": f"{request.method} {request.url.path}",
            "diagnostic_id": req_id,
            "detail": str(exc) or "Internal server error"
        }
    )

@app.on_event("startup")
def on_startup():
    try:
        seed_database()
    except Exception as e:
        print(f"Startup notice: {e}")

@app.get("/api/v1/system/status")
def system_status():
    return {
        "institution": settings.DEFAULT_INSTITUTION,
        "primary_color": settings.PRIMARY_COLOR,
        "accent_color": settings.ACCENT_COLOR,
        "llm_status": llm_service.get_status(),
        "database": settings.DATABASE_URL
    }

# Register API Routers
app.include_router(projects_router, prefix=settings.API_V1_STR)
app.include_router(agents_router, prefix=settings.API_V1_STR)
app.include_router(labs_router, prefix=settings.API_V1_STR)
app.include_router(teacher_router, prefix=settings.API_V1_STR)
app.include_router(researcher_router, prefix=settings.API_V1_STR)

# Serve Frontend static assets
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
assets_dir = os.path.join(frontend_dist, "assets")

if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/")
def serve_index():
    index_file = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "institution": settings.DEFAULT_INSTITUTION,
        "status": "OPERATIONAL",
        "llm_engine": llm_service.get_status()
    }
