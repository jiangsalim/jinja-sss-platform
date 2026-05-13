"""Director of Studies Dashboard API"""

from fastapi import APIRouter, Request
from app.database import get_db

router = APIRouter(prefix="/api/director-studies", tags=["Director of Studies"])


@router.get("/dashboard")
def dashboard():
    db = get_db()
    teachers = db.fetch_one("SELECT COUNT(*) as c FROM teachers")
    plans = db.fetch_one("SELECT COUNT(*) as c FROM lesson_plans")
    obs = db.fetch_one("SELECT COUNT(*) as c FROM performance_appraisals")
    return {"success": True, "data": {"teachers": teachers['c'] if teachers else 0, "lesson_plans": plans['c'] if plans else 0, "observations": obs['c'] if obs else 0}}


@router.get("/curriculum")
def curriculum():
    db = get_db()
    depts = db.fetch_all("""
        SELECT d.name, COUNT(DISTINCT ts.subject_id) as subjects, COUNT(DISTINCT ts.class_id) as classes
        FROM departments d LEFT JOIN teachers t ON d.id = t.department_id LEFT JOIN teacher_subjects ts ON t.id = ts.teacher_id GROUP BY d.id
    """)
    return {"success": True, "data": [dict(d) for d in depts] if depts else []}


@router.get("/teaching-quality")
def teaching_quality():
    return {"success": True, "data": {"overall": 4.2, "lesson_quality": 4.1, "management": 4.5, "engagement": 3.8}}


@router.get("/training")
def training():
    db = get_db()
    rows = db.fetch_all("SELECT * FROM training_sessions ORDER BY session_date DESC LIMIT 10")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/resources")
def resources():
    return {"success": True, "data": {"textbook_ratio": "1:2", "projectors": "8/12 working", "lab_kits": "70% functional"}}


@router.get("/benchmarking")
def benchmarking():
    return {"success": True, "data": {"math": 78, "physics": 74, "english": 91, "chemistry": 89, "national_avg": 72}}
