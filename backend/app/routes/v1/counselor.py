"""Counselor Dashboard API"""
from fastapi import APIRouter, Request, Query
from app.database import get_db

router = APIRouter(prefix="/api/counselor", tags=["Counselor"])

@router.get("/dashboard")
def dashboard():
    db = get_db()
    sessions = db.fetch_one("SELECT COUNT(*) as c FROM counseling_sessions WHERE date(session_date) = date('now')")
    active = db.fetch_one("SELECT COUNT(*) as c FROM counseling_sessions WHERE follow_up_date >= date('now')")
    return {"success": True, "data": {"today_sessions": sessions['c'] if sessions else 0, "active_cases": active['c'] if active else 0}}

@router.get("/schedule/today")
def today_schedule():
    db = get_db()
    rows = db.fetch_all("SELECT cs.*, u.full_name FROM counseling_sessions cs JOIN students s ON cs.student_id = s.id JOIN users u ON s.user_id = u.id WHERE date(cs.session_date) = date('now')")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}

@router.get("/referrals/pending")
def pending_referrals():
    return {"success": True, "data": []}

@router.get("/cases/active")
def active_cases():
    db = get_db()
    rows = db.fetch_all("SELECT cs.*, u.full_name FROM counseling_sessions cs JOIN students s ON cs.student_id = s.id JOIN users u ON s.user_id = u.id WHERE cs.follow_up_date >= date('now')")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}

@router.get("/at-risk")
def at_risk():
    return {"success": True, "data": []}

@router.get("/career-events")
def career_events():
    return {"success": True, "data": [{"title": "Career Fair 2026", "date": "2026-05-15"}]}
