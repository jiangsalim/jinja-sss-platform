"""Librarian API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/librarian", tags=["Librarian"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"total_books": 5245, "borrowed": 342, "overdue": 28, "visitors_today": 156}}
@router.get("/books")
def books(): return {"success": True, "data": []}
@router.get("/loans/active")
def active_loans(): return {"success": True, "data": []}
@router.get("/overdue")
def overdue(): return {"success": True, "data": []}
