"""Cleaner API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/cleaner", tags=["Cleaner"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"areas_assigned": 8, "completed": 3, "supplies": "OK"}}
