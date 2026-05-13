from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.config import settings
from app.utils.error_handler import register_error_handlers
from app.utils.response import success_response
from app.database import get_db

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, docs_url="/api/docs", redoc_url="/api/redoc")

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

register_error_handlers(app)

@app.get("/health")
def health():
    status = {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "version": settings.APP_VERSION}
    try:
        get_db().fetch_one("SELECT 1")
        status["database"] = "connected"
    except Exception as e:
        status["database"] = str(e)
        status["status"] = "degraded"
    return status

@app.get("/")
def root():
    return success_response(data={"app": settings.APP_NAME, "version": settings.APP_VERSION, "docs": "/api/docs"}, message="Jinja SSS Platform API is running")

@app.on_event("startup")
async def startup():
    print(f"Jinja SSS Platform v{settings.APP_VERSION} started on port {settings.PORT}")
