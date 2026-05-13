"""Admin Routes - audit log viewing"""

from fastapi import APIRouter, Depends, Query
from app.database import get_db

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/audit-log")
def get_audit_log(user_id: int = None, action: str = None, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT * FROM audit_log WHERE 1=1"
    params = []
    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)
    if action:
        query += " AND action = ?"
        params.append(action)
    total = db.fetch_one(f"SELECT COUNT(*) as c FROM ({query})", tuple(params))
    total_count = total['c'] if total else 0
    rows = db.fetch_all(f"{query} ORDER BY created_at DESC LIMIT ? OFFSET ?", tuple(params + [limit, (page-1)*limit]))
    return {"success": True, "data": [dict(r) for r in rows], "pagination": {"page": page, "limit": limit, "total": total_count}}
