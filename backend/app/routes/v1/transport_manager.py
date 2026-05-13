"""Transport Manager API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/transport-manager", tags=["Transport Manager"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"buses_active": "5/5", "drivers_on_duty": 4, "students_transported": 180}}
@router.get("/vehicles")
def vehicles(): return {"success": True, "data": []}
