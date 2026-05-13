"""Store Keeper API"""
from fastapi import APIRouter
router = APIRouter(prefix="/api/store-keeper", tags=["Store Keeper"])
@router.get("/dashboard")
def dashboard(): return {"success": True, "data": {"items_in_stock": 245, "low_stock": 8, "out_of_stock": 3}}
@router.get("/inventory/low-stock")
def low_stock(): return {"success": True, "data": []}
