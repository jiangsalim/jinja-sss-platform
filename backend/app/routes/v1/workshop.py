"""Workshop Technician API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/workshop", tags=["Workshop"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"tools_working": "85%", "pending_repairs": 4, "sessions_today": 3}}
@router.get("/schedule/today")
def schedule(): return {"success": True, "data": []}
@router.get("/equipment")
def equipment(): return {"success": True, "data": {"band_saw": "Working", "drill_press": "Under repair", "welding_machine": "Working"}}
