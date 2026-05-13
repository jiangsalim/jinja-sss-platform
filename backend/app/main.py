from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from datetime import datetime
import os, sqlite3

from app.config import settings
from app.utils.error_handler import register_error_handlers
from app.utils.response import success_response
from app.database import get_db
from app.middleware.auth import AuthMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.school import SchoolContextMiddleware
from app.middleware.sanitizer import SanitizerMiddleware
from app.middleware.audit import AuditMiddleware

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, docs_url="/api/docs", redoc_url="/api/redoc")

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(SanitizerMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(SchoolContextMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)

register_error_handlers(app)

@app.on_event("startup")
async def startup():
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "school.db")
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        schema_path = os.path.join(db_dir, "schema.sql")
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                conn.executescript(f.read())
            conn.commit()
        conn.close()
        print(f"Database created at {db_path}")
    print(f"Jinja SSS Platform v{settings.APP_VERSION} started")

@app.get("/setup-super-admin")
def setup_super_admin():
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
    db_path = os.path.join(db_dir, "school.db")
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("INSERT INTO users (id, username, email, password_hash, full_name, role, is_active, first_login) VALUES (999, 'superadmin', 'jaingsalim@gmail.com', 'temp123', 'Programmer Herman', 'super_admin', 1, 0)")
        conn.commit()
        result = "Super Admin created!"
    except:
        conn.execute("UPDATE users SET password_hash = 'temp123' WHERE username = 'superadmin'")
        conn.commit()
        result = "Super Admin password updated!"
    conn.close()
    return {"success": True, "message": result, "username": "superadmin", "password": "temp123"}

@app.get("/debug")
def debug():
    import glob as g
    files = []
    for root, dirs, filenames in os.walk("."):
        for f in filenames:
            if f.endswith('.db'):
                files.append(os.path.join(root, f))
    return {"cwd": os.getcwd(), "db_files": files}

@app.get("/health", tags=["System"])
def health():
    status = {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "version": settings.APP_VERSION}
    try:
        get_db().fetch_one("SELECT 1")
        status["database"] = "connected"
    except Exception as e:
        status["database"] = str(e)
        status["status"] = "degraded"
    return status

@app.get("/", tags=["System"])
def root():
    return success_response(data={"app": settings.APP_NAME, "version": settings.APP_VERSION}, message="Jinja SSS Platform API is running")

def custom_openapi():
    if app.openapi_schema: return app.openapi_schema
    schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
    schema["components"] = {"securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}}}
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi
