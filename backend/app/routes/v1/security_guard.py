"""Security Guard API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/security-guard", tags=["Security Guard"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"shift": "06-14", "checkpoints": "3/5", "visitors_today": 12}}
@router.get("/patrol/route")
def patrol(): return {"success": True, "data": []}
