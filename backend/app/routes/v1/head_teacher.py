"""Head Teacher Dashboard API"""

from fastapi import APIRouter, HTTPException, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/headteacher", tags=["Head Teacher"])


@router.get("/dashboard")
def dashboard(request: Request):
    db = get_db()
    students = db.fetch_one("SELECT COUNT(*) as c FROM students")
    teachers = db.fetch_one("SELECT COUNT(*) as c FROM teachers")
    attendance = db.fetch_one("SELECT ROUND(AVG(CASE WHEN status='present' THEN 1.0 ELSE 0.0 END)*100,1) as rate FROM attendance WHERE date = date('now')")
    fees = db.fetch_one("SELECT COALESCE(SUM(amount),0) as total FROM fee_payments")
    
    return {"success": True, "data": {
        "students": students['c'] if students else 0,
        "teachers": teachers['c'] if teachers else 0,
        "attendance_rate": attendance['rate'] if attendance else 0,
        "fees_collected": fees['total'] if fees else 0
    }}


@router.get("/pending-approvals")
def pending_approvals():
    db = get_db()
    leave = db.fetch_all("SELECT * FROM staff_leave WHERE status='pending' LIMIT 10")
    return {"success": True, "data": {"leave_requests": [dict(l) for l in leave] if leave else []}}


@router.get("/departments")
def departments():
    db = get_db()
    depts = db.fetch_all("""
        SELECT d.name, COUNT(t.id) as teacher_count,
               (SELECT COUNT(*) FROM students s JOIN teacher_subjects ts ON s.class_id = ts.class_id JOIN teachers t2 ON ts.teacher_id = t2.id WHERE t2.department_id = d.id) as student_count
        FROM departments d LEFT JOIN teachers t ON d.id = t.department_id GROUP BY d.id
    """)
    return {"success": True, "data": [dict(d) for d in depts] if depts else []}


@router.get("/staff-attendance")
def staff_attendance():
    db = get_db()
    rows = db.fetch_one("""
        SELECT COUNT(*) as total, SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present
        FROM staff_attendance WHERE date = date('now')
    """)
    return {"success": True, "data": dict(rows) if rows else {}}


@router.post("/announcements")
def create_announcement(request: Request):
    return {"success": True, "message": "Announcement created"}


@router.get("/announcements")
def get_announcements(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT * FROM announcements ORDER BY created_at DESC"
    count_query = "SELECT COUNT(*) as c FROM announcements"
    result = PaginationHelper.paginate_query(query, count_query, (), page, limit)
    return {"success": True, **result}
