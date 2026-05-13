"""Jinja SSS Platform - Main Application Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from datetime import datetime
import os

from app.config import settings
from app.utils.error_handler import register_error_handlers
from app.utils.response import success_response
from app.database import get_db
from app.middleware.auth import AuthMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.school import SchoolContextMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    contact={"name": "Jinja SSS IT Team", "email": "support@jinjasss.sc.ug"},
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(SchoolContextMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)

register_error_handlers(app)


@app.get("/health", tags=["System"])
def health():
    status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    }
    try:
        get_db().fetch_one("SELECT 1")
        status["database"] = "connected"
    except Exception as e:
        status["database"] = str(e)
        status["status"] = "degraded"
    return status


@app.get("/", tags=["System"])
def root():
    return success_response(
        data={"app": settings.APP_NAME, "version": settings.APP_VERSION, "docs": "/api/docs"},
        message="Jinja SSS Platform API is running"
    )


@app.on_event("startup")
async def startup():
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} started on port {settings.PORT}")
    print(f"📖 API Docs: http://localhost:{settings.PORT}/api/docs")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
    schema["components"] = schema.get("components", {})
    schema["components"]["securitySchemes"] = {"BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}}
    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi
