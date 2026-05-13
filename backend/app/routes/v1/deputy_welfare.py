"""Deputy Head Welfare Dashboard API"""

from fastapi import APIRouter, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/deputy-welfare", tags=["Deputy Head Welfare"])


@router.get("/dashboard")
def dashboard():
    db = get_db()
    incidents_today = db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE date(reported_at) = date('now')")
    pending = db.fetch_one("SELECT COUNT(*) as c FROM incidents WHERE status='pending'")
    staff_leave = db.fetch_one("SELECT COUNT(*) as c FROM staff_leave WHERE date('now') BETWEEN start_date AND end_date")
    return {"success": True, "data": {"incidents_today": incidents_today['c'] if incidents_today else 0, "pending_cases": pending['c'] if pending else 0, "staff_on_leave": staff_leave['c'] if staff_leave else 0}}


@router.get("/incidents/today")
def incidents_today():
    db = get_db()
    rows = db.fetch_all("SELECT i.*, u.full_name as student_name FROM incidents i JOIN students s ON i.student_id = s.id JOIN users u ON s.user_id = u.id WHERE date(i.reported_at) = date('now')")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/discipline/pending")
def pending_cases():
    db = get_db()
    rows = db.fetch_all("SELECT * FROM incidents WHERE status='pending'")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/staff-leave")
def staff_on_leave():
    db = get_db()
    rows = db.fetch_all("SELECT sl.*, u.full_name FROM staff_leave sl JOIN teachers t ON sl.staff_id = t.id JOIN users u ON t.user_id = u.id WHERE date('now') BETWEEN sl.start_date AND sl.end_date")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/sickbay")
def sick_bay():
    db = get_db()
    today = db.fetch_one("SELECT COUNT(*) as c FROM sick_bay_visits WHERE date(arrival_time) = date('now')")
    current = db.fetch_one("SELECT COUNT(*) as c FROM sick_bay_visits WHERE date(arrival_time) = date('now') AND departure_time IS NULL")
    return {"success": True, "data": {"visits_today": today['c'] if today else 0, "current_patients": current['c'] if current else 0}}


@router.get("/complaints")
def parent_complaints():
    db = get_db()
    rows = db.fetch_all("SELECT * FROM parent_complaints WHERE status='pending'")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}
