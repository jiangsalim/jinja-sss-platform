"""HR Officer Dashboard API"""

from fastapi import APIRouter, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/hr", tags=["HR"])


@router.get("/dashboard")
def dashboard():
    db = get_db()
    staff = db.fetch_one("SELECT COUNT(*) as c FROM teachers")
    leave = db.fetch_one("SELECT COUNT(*) as c FROM staff_leave WHERE status='pending'")
    attendance = db.fetch_one("""
        SELECT COUNT(*) as total, SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present
        FROM staff_attendance WHERE date = date('now')
    """)
    return {"success": True, "data": {"total_staff": staff['c'] if staff else 0, "pending_leave": leave['c'] if leave else 0, "attendance_rate": round((attendance['present']/attendance['total'])*100,1) if attendance and attendance['total'] > 0 else 0}}


@router.get("/staff")
def staff_list(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT t.*, u.full_name, u.email, u.phone FROM teachers t JOIN users u ON t.user_id = u.id"
    count_query = "SELECT COUNT(*) as c FROM teachers"
    result = PaginationHelper.paginate_query(query, count_query, (), page, limit)
    return {"success": True, **result}


@router.get("/leave/pending")
def pending_leave():
    db = get_db()
    rows = db.fetch_all("SELECT sl.*, u.full_name FROM staff_leave sl JOIN teachers t ON sl.staff_id = t.id JOIN users u ON t.user_id = u.id WHERE sl.status='pending'")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/attendance/today")
def staff_attendance_today():
    db = get_db()
    rows = db.fetch_one("""
        SELECT COUNT(*) as total, SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present,
               SUM(CASE WHEN status='absent' THEN 1 ELSE 0 END) as absent,
               SUM(CASE WHEN status='late' THEN 1 ELSE 0 END) as late
        FROM staff_attendance WHERE date = date('now')
    """)
    return {"success": True, "data": dict(rows) if rows else {}}


@router.get("/appraisals/pending")
def pending_appraisals():
    db = get_db()
    rows = db.fetch_all("SELECT pa.*, u.full_name FROM performance_appraisals pa JOIN teachers t ON pa.teacher_id = t.id JOIN users u ON t.user_id = u.id WHERE pa.status='draft'")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/recruitment")
def recruitment():
    return {"success": True, "data": {"open_positions": 3, "applications": 12}}


@router.get("/training")
def training():
    db = get_db()
    rows = db.fetch_all("SELECT * FROM training_sessions ORDER BY session_date DESC LIMIT 10")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/contracts")
def contracts():
    return {"success": True, "data": []}
