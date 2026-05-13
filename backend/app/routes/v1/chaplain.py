"""Chaplain Dashboard API"""
from fastapi import APIRouter
from app.database import get_db

router = APIRouter(prefix="/api/chaplain", tags=["Chaplain"])

@router.get("/dashboard")
def dashboard():
    return {"success": True, "data": {"services_this_week": 5, "choir_members": 45, "counseling_sessions": 8}}

@router.get("/assembly/schedule")
def assembly_schedule():
    return {"success": True, "data": []}

@router.get("/services")
def services():
    return {"success": True, "data": []}

@router.get("/choir")
def choir():
    return {"success": True, "data": {"members": 45, "rehearsals": {"monday": "3PM", "wednesday": "3PM", "friday": "2PM"}}}

@router.get("/counseling/pending")
def pending_spiritual_counseling():
    return {"success": True, "data": []}

@router.get("/events")
def religious_events():
    return {"success": True, "data": [{"name": "Easter Service", "date": "2026-04-30"}]}
