"""Head of Security API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/head-security", tags=["Head Security"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"guards_on_duty": 6, "cctv_online": "12/12", "incidents": 0}}
@router.get("/roster/today")
def roster(): return {"success": True, "data": []}
