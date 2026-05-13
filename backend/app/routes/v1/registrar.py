"""Academic Registrar Dashboard API"""

from fastapi import APIRouter, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/registrar", tags=["Registrar"])


@router.get("/dashboard")
def dashboard():
    db = get_db()
    total = db.fetch_one("SELECT COUNT(*) as c FROM students")
    new_this_term = db.fetch_one("SELECT COUNT(*) as c FROM students WHERE enrollment_year = 2026")
    transfers = db.fetch_one("SELECT COUNT(*) as c FROM student_transfers")
    return {"success": True, "data": {"total_students": total['c'] if total else 0, "new_this_term": new_this_term['c'] if new_this_term else 0, "transfers": transfers['c'] if transfers else 0}}


@router.get("/students")
def students(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT s.*, u.full_name, c.name as class_name FROM students s JOIN users u ON s.user_id = u.id JOIN classes c ON s.class_id = c.id"
    count_query = "SELECT COUNT(*) as c FROM students"
    result = PaginationHelper.paginate_query(query, count_query, (), page, limit)
    return {"success": True, **result}


@router.get("/students/{student_id}")
def student_detail(student_id: int):
    db = get_db()
    s = db.fetch_one("SELECT s.*, u.full_name, u.email, u.phone FROM students s JOIN users u ON s.user_id = u.id WHERE s.id = ?", (student_id,))
    if not s:
        return {"success": False, "error": {"code": "STUDENT_NOT_FOUND"}}
    return {"success": True, "data": dict(s)}


@router.get("/admissions/pending")
def pending_admissions():
    return {"success": True, "data": []}


@router.get("/transfers")
def transfers():
    db = get_db()
    rows = db.fetch_all("SELECT st.*, u.full_name FROM student_transfers st JOIN students s ON st.student_id = s.id JOIN users u ON s.user_id = u.id")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/class-placement")
def class_placement():
    db = get_db()
    rows = db.fetch_all("SELECT c.name, c.capacity, c.current_enrollment, (c.capacity - c.current_enrollment) as available FROM classes c")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}
