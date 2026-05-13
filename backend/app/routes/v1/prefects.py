"""Prefect Leadership APIs"""
from fastapi import APIRouter
router = APIRouter(prefix="/api", tags=["Prefects"])

@router.get("/prefect-coordinator/dashboard")
def coordinator(): return {"success": True, "data": {"total_prefects": 45, "on_duty": 12, "reports_this_week": 8}}

@router.get("/head-prefect/dashboard")
def head_prefect(): return {"success": True, "data": {"team_size": 45, "on_duty": 12, "reports_received": "8/12"}}

@router.get("/dept-prefect/dashboard")
def dept_prefect(): return {"success": True, "data": {"class_prefects": 6, "reports_received": "4/6", "students": 180}}

@router.get("/class-prefect/dashboard")
def class_prefect(): return {"success": True, "data": {"students": 45, "present": 42, "homework_collected": "38/45"}}
