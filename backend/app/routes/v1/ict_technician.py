"""ICT Technician API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/ict-technician", tags=["ICT Technician"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"my_tickets": 3, "open_tickets": 8, "completed_today": 4}}
