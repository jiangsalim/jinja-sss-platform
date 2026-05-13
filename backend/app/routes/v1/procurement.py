"""Procurement Officer API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/procurement", tags=["Procurement"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"active_orders": 8, "pending_approvals": 3, "budget_remaining": "UGX 12.5M"}}
@router.get("/orders/active")
def orders(): return {"success": True, "data": []}
