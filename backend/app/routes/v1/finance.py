"""Finance Officer Dashboard API"""

from fastapi import APIRouter, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/finance", tags=["Finance"])


@router.get("/dashboard")
def dashboard():
    db = get_db()
    collected = db.fetch_one("SELECT COALESCE(SUM(amount),0) as total FROM fee_payments")
    expenses = db.fetch_one("SELECT COALESCE(SUM(amount),0) as total FROM expenses")
    return {"success": True, "data": {"collected": collected['total'] if collected else 0, "expenses": expenses['total'] if expenses else 0, "collection_rate": 82}}


@router.get("/fees/collection")
def fee_collection():
    db = get_db()
    rows = db.fetch_all("""
        SELECT c.name as class_name, COUNT(DISTINCT s.id) as students,
               COALESCE(SUM(fp.amount),0) as collected
        FROM classes c LEFT JOIN students s ON c.id = s.class_id LEFT JOIN fee_payments fp ON s.id = fp.student_id GROUP BY c.id
    """)
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/fees/overdue")
def overdue_fees():
    db = get_db()
    rows = db.fetch_all("SELECT * FROM parent_fee_balance WHERE balance > 0 ORDER BY balance DESC LIMIT 20")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/transactions/today")
def today_transactions():
    db = get_db()
    rows = db.fetch_all("SELECT * FROM fee_payments WHERE date(payment_date) = date('now')")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/expenses")
def expenses(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT * FROM expenses ORDER BY expense_date DESC"
    count_query = "SELECT COUNT(*) as c FROM expenses"
    result = PaginationHelper.paginate_query(query, count_query, (), page, limit)
    return {"success": True, **result}


@router.get("/budget/vs-actual")
def budget_vs_actual():
    return {"success": True, "data": {"salaries": {"budget": 25000000, "actual": 25000000}, "utilities": {"budget": 3000000, "actual": 2800000}}}


@router.get("/payroll")
def payroll():
    db = get_db()
    rows = db.fetch_all("SELECT * FROM payroll ORDER BY year DESC, month DESC LIMIT 20")
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}
