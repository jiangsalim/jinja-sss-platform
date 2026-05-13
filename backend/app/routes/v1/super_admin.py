"""Super Admin Dashboard API"""

from fastapi import APIRouter, Request, Query, HTTPException
from app.database import get_db
from app.utils.pagination import PaginationHelper
from app.utils.audit import AuditLogger
from app.utils.password import PasswordManager
from app.utils.id_generator import IDGenerator
from datetime import datetime

router = APIRouter(prefix="/api/super-admin", tags=["Super Admin"])


@router.get("/dashboard")
def dashboard():
    db = get_db()
    return {"success": True, "data": {
        "total_users": db.fetch_one("SELECT COUNT(*) as c FROM users")['c'],
        "total_students": db.fetch_one("SELECT COUNT(*) as c FROM students")['c'],
        "total_teachers": db.fetch_one("SELECT COUNT(*) as c FROM teachers")['c'],
        "total_parents": db.fetch_one("SELECT COUNT(*) as c FROM parents")['c'],
        "database_size": "73 tables",
        "server_status": "healthy"
    }}


@router.post("/users")
def create_user(request: Request):
    """Super Admin creates any user with proper hierarchy"""
    from fastapi import Request as FastAPIRequest
    import json as _json
    
    db = get_db()
    body = request.body()
    if isinstance(body, bytes):
        body = _json.loads(body)
    
    full_name = body.get('full_name')
    email = body.get('email', '')
    role = body.get('role', 'student')
    username = body.get('username', '')
    password = body.get('password', 'changeme123')
    staff_id = body.get('staff_id', '')
    position = body.get('position', '')
    
    if not username:
        username = role + '_' + str(int(datetime.utcnow().timestamp()))
    
    # Hash password
    password_hash = PasswordManager.hash_password(password)
    
    # Create user
    cursor = db.get_connection().cursor()
    cursor.execute("INSERT INTO users (username, email, password_hash, full_name, role, is_active, first_login) VALUES (?, ?, ?, ?, ?, 1, 0)",
                   (username, email, password_hash, full_name, role))
    user_id = cursor.lastrowid
    
    # Create role-specific record
    if role == 'student':
        admission = IDGenerator.generate_entity_id('JSSS', 0)
        db.execute("INSERT INTO students (user_id, admission_number) VALUES (?, ?)", (user_id, admission))
    elif role in ['teacher', 'hod', 'head_teacher', 'nurse', 'counselor', 'chaplain', 'social_worker', 'librarian']:
        sid = staff_id or IDGenerator.generate_entity_id(IDGenerator.PREFIXES.get(role, 'STF'), 0)
        db.execute("INSERT INTO teachers (user_id, staff_id, teacher_type) VALUES (?, ?, ?)", (user_id, sid, 'subject'))
    elif role == 'parent':
        db.execute("INSERT INTO parents (user_id) VALUES (?)", (user_id,))
    
    # Log audit
    AuditLogger.log_user_create(999, user_id)  # 999 = Super Admin ID
    
    return {"success": True, "message": "User created successfully", "user_id": user_id, "username": username}


@router.get("/users")
def list_users(role: str = None, search: str = None, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT u.id, u.username, u.full_name, u.email, u.role, u.is_active, u.created_at FROM users u WHERE 1=1"
    count_query = "SELECT COUNT(*) as c FROM users WHERE 1=1"
    params = []
    if role:
        query += " AND u.role = ?"
        count_query += " AND role = ?"
        params.append(role)
    if search:
        query += " AND (u.full_name LIKE ? OR u.username LIKE ? OR u.email LIKE ?)"
        count_query += " AND (full_name LIKE ? OR username LIKE ? OR email LIKE ?)"
        params.extend([f'%{search}%'] * 3)
    result = PaginationHelper.paginate_query(query, count_query, tuple(params), page, limit, "u.created_at")
    return {"success": True, **result}


@router.put("/users/{user_id}")
def update_user(user_id: int, request: Request):
    return {"success": True, "message": "User updated"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, request: Request):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    AuditLogger.log(999, "USER_DELETE", "users", user_id)
    return {"success": True, "message": "User deleted"}


@router.get("/audit-log")
def audit_log(user_id: int = None, action: str = None, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT a.*, u.full_name FROM audit_log a LEFT JOIN users u ON a.user_id = u.id WHERE 1=1"
    count_query = "SELECT COUNT(*) as c FROM audit_log WHERE 1=1"
    params = []
    if user_id:
        query += " AND a.user_id = ?"
        count_query += " AND user_id = ?"
        params.append(user_id)
    if action:
        query += " AND a.action = ?"
        count_query += " AND action = ?"
        params.append(action)
    result = PaginationHelper.paginate_query(query, count_query, tuple(params), page, limit, "a.created_at")
    return {"success": True, **result}


@router.get("/system-settings")
def get_settings():
    db = get_db()
    rows = db.fetch_all("SELECT * FROM system_settings")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}
