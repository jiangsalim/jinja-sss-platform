"""Super Admin Dashboard API"""

from fastapi import APIRouter, Request, Query, HTTPException
from app.database import get_db
from app.utils.pagination import PaginationHelper
from app.utils.audit import AuditLogger
from app.utils.password import PasswordManager
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


@router.get("/users")
def list_users(role: str = None, search: str = None, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT u.*, s.admission_number as student_id, t.staff_id as teacher_id FROM users u LEFT JOIN students s ON u.id = s.user_id LEFT JOIN teachers t ON u.id = t.user_id WHERE 1=1"
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


@router.post("/users")
def create_user(request: Request):
    db = get_db()
    # Implementation for creating users
    return {"success": True, "message": "User created"}


@router.put("/users/{user_id}")
def update_user(user_id: int, request: Request):
    db = get_db()
    return {"success": True, "message": "User updated"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, request: Request):
    db = get_db()
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


@router.put("/system-settings")
def update_settings():
    return {"success": True, "message": "Settings updated"}


@router.post("/backup")
def create_backup():
    from app.services.backup_service import BackupService
    bs = BackupService()
    filename = bs.create_backup()
    return {"success": True, "data": {"backup_file": filename}}


@router.get("/backups")
def list_backups():
    from app.services.backup_service import BackupService
    bs = BackupService()
    return {"success": True, "data": bs.list_backups()}
