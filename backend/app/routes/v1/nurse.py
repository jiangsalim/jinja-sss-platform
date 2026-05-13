"""Nurse Dashboard API"""
from fastapi import APIRouter, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/nurse", tags=["Nurse"])

@router.get("/dashboard")
def dashboard():
    db = get_db()
    today = db.fetch_one("SELECT COUNT(*) as c FROM sick_bay_visits WHERE date(arrival_time) = date('now')")
    current = db.fetch_one("SELECT COUNT(*) as c FROM sick_bay_visits WHERE date(arrival_time) = date('now') AND departure_time IS NULL")
    return {"success": True, "data": {"visits_today": today['c'] if today else 0, "current_patients": current['c'] if current else 0}}

@router.get("/sickbay/current")
def current_patients():
    db = get_db()
    rows = db.fetch_all("SELECT sbv.*, u.full_name FROM sick_bay_visits sbv JOIN students s ON sbv.student_id = s.id JOIN users u ON s.user_id = u.id WHERE date(sbv.arrival_time) = date('now') AND sbv.departure_time IS NULL")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}

@router.get("/visits/today")
def visits_today():
    db = get_db()
    rows = db.fetch_all("SELECT sbv.*, u.full_name FROM sick_bay_visits sbv JOIN students s ON sbv.student_id = s.id JOIN users u ON s.user_id = u.id WHERE date(sbv.arrival_time) = date('now') ORDER BY sbv.arrival_time DESC")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}

@router.get("/medication/schedule")
def medication_schedule():
    db = get_db()
    rows = db.fetch_all("SELECT ms.*, u.full_name FROM medication_schedule ms JOIN students s ON ms.student_id = s.id JOIN users u ON s.user_id = u.id WHERE ms.start_date <= date('now') AND ms.end_date >= date('now')")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}

@router.get("/students/{student_id}/medical")
def student_medical(student_id: int):
    db = get_db()
    row = db.fetch_one("SELECT smr.*, u.full_name FROM student_medical_records smr JOIN students s ON smr.student_id = s.id JOIN users u ON s.user_id = u.id WHERE smr.student_id = ?", (student_id,))
    return {"success": True, "data": dict(row) if row else {}}

@router.get("/inventory")
def inventory():
    return {"success": True, "data": {"paracetamol": 45, "bandages": 12, "thermometers": 2}}

@router.get("/health-trends")
def health_trends():
    db = get_db()
    rows = db.fetch_all("SELECT date(arrival_time) as day, COUNT(*) as visits FROM sick_bay_visits GROUP BY date(arrival_time) ORDER BY day DESC LIMIT 7")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}
