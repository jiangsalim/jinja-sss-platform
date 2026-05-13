"""Deputy Head Academics Dashboard API"""

from fastapi import APIRouter, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/deputy-academics", tags=["Deputy Head Academics"])


@router.get("/dashboard")
def dashboard():
    db = get_db()
    teachers = db.fetch_one("SELECT COUNT(*) as c FROM teachers")
    subjects = db.fetch_one("SELECT COUNT(*) as c FROM subjects")
    pending = db.fetch_one("SELECT COUNT(*) as c FROM lesson_plans WHERE status='pending'")
    return {"success": True, "data": {"teachers": teachers['c'] if teachers else 0, "subjects": subjects['c'] if subjects else 0, "pending_approvals": pending['c'] if pending else 0}}


@router.get("/exams")
def exam_status():
    return {"success": True, "data": {"scheduling": "done", "papers": "in_progress", "conduct": "pending"}}


@router.get("/timetable")
def timetable_status():
    db = get_db()
    classes = db.fetch_all("SELECT c.name, COUNT(t.id) as lessons FROM classes c LEFT JOIN timetable t ON c.id = t.class_id GROUP BY c.id")
    return {"success": True, "data": [dict(c) for c in classes] if classes else []}


@router.get("/lesson-plans")
def lesson_plan_compliance():
    db = get_db()
    depts = db.fetch_all("""
        SELECT d.name, COUNT(lp.id) as total,
               SUM(CASE WHEN lp.status='approved' THEN 1 ELSE 0 END) as approved
        FROM departments d LEFT JOIN teachers t ON d.id = t.department_id LEFT JOIN lesson_plans lp ON t.id = lp.teacher_id GROUP BY d.id
    """)
    return {"success": True, "data": [dict(d) for d in depts] if depts else []}


@router.get("/observations")
def observations():
    return {"success": True, "data": []}
