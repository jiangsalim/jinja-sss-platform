"""Chef API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/chef", tags=["Chef"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"meals_today": "Breakfast", "students_served": 450, "food_cost": "UGX 1.2M"}}
@router.get("/menu/today")
def menu(): return {"success": True, "data": {"breakfast": "Porridge, Bread", "lunch": "Rice, Beans", "supper": "Matooke, Groundnuts"}}
