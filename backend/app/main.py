from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from datetime import datetime

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

# Import ALL routes
from app.routes.v1.admin import router as r1; app.include_router(r1)
from app.routes.v1.auth import router as r2; app.include_router(r2)
from app.routes.v1.students import router as r3; app.include_router(r3)
from app.routes.v1.parents import router as r4; app.include_router(r4)
from app.routes.v1.teachers import router as r5; app.include_router(r5)
from app.routes.v1.hod import router as r6; app.include_router(r6)
from app.routes.v1.head_teacher import router as r7; app.include_router(r7)
from app.routes.v1.deputy_academics import router as r8; app.include_router(r8)
from app.routes.v1.deputy_welfare import router as r9; app.include_router(r9)
from app.routes.v1.registrar import router as r10; app.include_router(r10)
from app.routes.v1.director_studies import router as r11; app.include_router(r11)
from app.routes.v1.finance import router as r12; app.include_router(r12)
from app.routes.v1.hr import router as r13; app.include_router(r13)
from app.routes.v1.nurse import router as r14; app.include_router(r14)
from app.routes.v1.counselor import router as r15; app.include_router(r15)
from app.routes.v1.chaplain import router as r16; app.include_router(r16)
from app.routes.v1.social_worker import router as r17; app.include_router(r17)
from app.routes.v1.lab_science import router as r18; app.include_router(r18)
from app.routes.v1.lab_computer import router as r19; app.include_router(r19)
from app.routes.v1.workshop import router as r20; app.include_router(r20)
from app.routes.v1.receptionist import router as r21; app.include_router(r21)
from app.routes.v1.records_clerk import router as r22; app.include_router(r22)
from app.routes.v1.procurement import router as r23; app.include_router(r23)
from app.routes.v1.store_keeper import router as r24; app.include_router(r24)
from app.routes.v1.head_security import router as r25; app.include_router(r25)
from app.routes.v1.security_guard import router as r26; app.include_router(r26)
from app.routes.v1.maintenance import router as r27; app.include_router(r27)
from app.routes.v1.groundskeeper import router as r28; app.include_router(r28)
from app.routes.v1.cleaner import router as r29; app.include_router(r29)
from app.routes.v1.chef import router as r30; app.include_router(r30)
from app.routes.v1.kitchen_staff import router as r31; app.include_router(r31)
from app.routes.v1.transport_manager import router as r32; app.include_router(r32)
from app.routes.v1.bus_driver import router as r33; app.include_router(r33)
from app.routes.v1.ict_manager import router as r34; app.include_router(r34)
from app.routes.v1.ict_technician import router as r35; app.include_router(r35)
from app.routes.v1.librarian import router as r36; app.include_router(r36)
from app.routes.v1.library_assistant import router as r37; app.include_router(r37)
from app.routes.v1.prefects import router as r38; app.include_router(r38)
from app.routes.v1.alumni import router as r39; app.include_router(r39)

from app.routes.v1.super_admin import router as super_admin_router
app.include_router(super_admin_router)


@app.get("/setup-super-admin")
def setup_super_admin():
    """One-time super admin setup - DELETE after use"""
    import sqlite3, hashlib, os
    conn = sqlite3.connect('database/school.db')
    password = "HermanKing2026!"
    salt = os.urandom(16).hex()
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest() + ":" + salt
    try:
        conn.execute("INSERT INTO users (id, username, email, password_hash, full_name, role, is_active, first_login) VALUES (999, 'superadmin', 'jaingsalim@gmail.com', ?, 'Programmer Herman', 'super_admin', 1, 0)", (password_hash,))
        conn.commit()
        result = "Super Admin created!"
    except:
        conn.execute("UPDATE users SET password_hash = ? WHERE username = 'superadmin'", (password_hash,))
        conn.commit()
        result = "Super Admin password updated!"
    conn.close()
    return {"success": True, "message": result, "username": "superadmin", "password": "HermanKing2026!"}


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

@app.on_event("startup")
async def startup():
    print(f"Jinja SSS Platform v{settings.APP_VERSION} started with 39 route modules")

def custom_openapi():
    if app.openapi_schema: return app.openapi_schema
    schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
    schema["components"] = {"securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}}}
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi
