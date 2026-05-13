"""Kitchen Staff API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/kitchen-staff", tags=["Kitchen Staff"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"tasks_today": 8, "completed": 4, "meal": "Lunch"}}
