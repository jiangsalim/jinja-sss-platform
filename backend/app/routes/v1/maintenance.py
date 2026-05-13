"""Maintenance Head API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/maintenance", tags=["Maintenance"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"open_orders": 12, "in_progress": 5, "urgent": 2}}
@router.get("/work-orders/pending")
def work_orders(): return {"success": True, "data": []}
