"""Social Worker Dashboard API"""
from fastapi import APIRouter, Request
from app.database import get_db

router = APIRouter(prefix="/api/social-worker", tags=["Social Worker"])

@router.get("/dashboard")
def dashboard():
    db = get_db()
    cases = db.fetch_one("SELECT COUNT(*) as c FROM welfare_cases WHERE status='active'")
    visits = db.fetch_one("SELECT COUNT(*) as c FROM home_visits")
    return {"success": True, "data": {"active_cases": cases['c'] if cases else 0, "home_visits": visits['c'] if visits else 0}}

@router.get("/cases/active")
def active_cases():
    db = get_db()
    rows = db.fetch_all("SELECT wc.*, u.full_name FROM welfare_cases wc JOIN students s ON wc.student_id = s.id JOIN users u ON s.user_id = u.id WHERE wc.status='active'")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}

@router.get("/home-visits/schedule")
def home_visit_schedule():
    db = get_db()
    rows = db.fetch_all("SELECT hv.*, u.full_name FROM home_visits hv JOIN students s ON hv.student_id = s.id JOIN users u ON s.user_id = u.id ORDER BY hv.visit_date DESC LIMIT 10")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}

@router.get("/resources/inventory")
def resources():
    return {"success": True, "data": {"uniforms": 25, "shoes": 12, "backpacks": 30}}

@router.get("/partners")
def partners():
    return {"success": True, "data": ["Jinja Probation Office", "Save the Children", "Uganda Red Cross"]}

@router.get("/child-protection")
def child_protection():
    return {"success": True, "data": []}
