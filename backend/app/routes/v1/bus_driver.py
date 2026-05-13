"""Bus Driver API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/bus-driver", tags=["Bus Driver"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"bus": "BUS-01", "route": "North", "students_onboard": 45, "fuel": "65%"}}
@router.get("/route/today")
def route(): return {"success": True, "data": []}
