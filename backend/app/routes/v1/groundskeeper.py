"""Groundskeeper API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/groundskeeper", tags=["Groundskeeper"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"tasks_today": 6, "completed": 3, "sports_field": "Ready"}}
