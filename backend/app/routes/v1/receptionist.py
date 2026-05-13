"""Receptionist API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/receptionist", tags=["Receptionist"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"visitors_today": 12, "expected_today": 8, "packages": 5}}
@router.get("/visitors/today")
def visitors(): return {"success": True, "data": []}
