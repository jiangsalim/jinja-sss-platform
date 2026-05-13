"""Parent Dashboard API Routes"""

from fastapi import APIRouter, HTTPException, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/parent", tags=["Parent"])


def get_current_parent(request: Request):
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    db = get_db()
    parent = db.fetch_one("SELECT * FROM parents WHERE user_id = ?", (request.state.user_id,))
    if not parent:
        raise HTTPException(status_code=404, detail="Parent record not found")
    return dict(parent)


@router.get("/dashboard")
def dashboard(request: Request):
    parent = get_current_parent(request)
    db = get_db()
    children = db.fetch_all("""
        SELECT s.id, s.admission_number, u.full_name, c.name as class_name,
               s.stream_id, pfs.balance as fees_due
        FROM parent_student_links psl
        JOIN students s ON psl.student_id = s.id
        JOIN users u ON s.user_id = u.id
        JOIN classes c ON s.class_id = c.id
        LEFT JOIN parent_fee_balance pfs ON s.id = pfs.student_id
        WHERE psl.parent_id = ?
    """, (parent['id'],))
    return {"success": True, "data": {"parent": parent, "children": [dict(c) for c in children] if children else []}}


@router.get("/children/{child_id}/grades")
def get_child_grades(child_id: int, request: Request, term_id: int = None, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    parent = get_current_parent(request)
    db = get_db()
    link = db.fetch_one("SELECT * FROM parent_student_links WHERE parent_id = ? AND student_id = ?", (parent['id'], child_id))
    if not link:
        raise HTTPException(status_code=403, detail="Not your child")
    query = "SELECT g.*, s.name as subject_name FROM grades g JOIN subjects s ON g.subject_id = s.id WHERE g.student_id = ?"
    count_query = "SELECT COUNT(*) as c FROM grades WHERE student_id = ?"
    params = [child_id]
    if term_id:
        query += " AND g.term_id = ?"
        count_query += " AND term_id = ?"
        params.append(term_id)
    result = PaginationHelper.paginate_query(query, count_query, tuple(params), page, limit, "g.recorded_at")
    student = db.fetch_one("SELECT u.full_name FROM students s JOIN users u ON s.user_id = u.id WHERE s.id = ?", (child_id,))
    return {"success": True, "child": dict(student) if student else {}, **result}


@router.get("/children/{child_id}/attendance")
def get_child_attendance(child_id: int, request: Request, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    parent = get_current_parent(request)
    db = get_db()
    link = db.fetch_one("SELECT * FROM parent_student_links WHERE parent_id = ? AND student_id = ?", (parent['id'], child_id))
    if not link:
        raise HTTPException(status_code=403, detail="Not your child")
    total = db.fetch_one("SELECT COUNT(*) as c FROM attendance WHERE student_id = ?", (child_id,))
    present = db.fetch_one("SELECT COUNT(*) as c FROM attendance WHERE student_id = ? AND status = 'present'", (child_id,))
    pct = round((present['c'] / total['c']) * 100) if total and total['c'] > 0 else 0
    query = "SELECT date, status, period FROM attendance WHERE student_id = ?"
    count_query = "SELECT COUNT(*) as c FROM attendance WHERE student_id = ?"
    result = PaginationHelper.paginate_query(query, count_query, (child_id,), page, limit, "date")
    result["summary"] = {"attendance_percentage": pct}
    return {"success": True, **result}


@router.get("/children/{child_id}/fees")
def get_child_fees(child_id: int, request: Request):
    parent = get_current_parent(request)
    db = get_db()
    link = db.fetch_one("SELECT * FROM parent_student_links WHERE parent_id = ? AND student_id = ?", (parent['id'], child_id))
    if not link:
        raise HTTPException(status_code=403, detail="Not your child")
    balance = db.fetch_one("SELECT * FROM parent_fee_balance WHERE student_id = ?", (child_id,))
    payments = db.fetch_all("SELECT * FROM fee_payments WHERE student_id = ? ORDER BY payment_date DESC LIMIT 10", (child_id,))
    return {"success": True, "data": {"balance": dict(balance) if balance else {}, "payments": [dict(p) for p in payments] if payments else []}}


@router.get("/messages")
def get_messages(request: Request, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    db = get_db()
    query = """SELECT m.id, u.full_name as sender, m.message, m.sent_at, m.is_read FROM messages m
               JOIN conversations c ON m.conversation_id = c.id JOIN users u ON m.sender_id = u.id
               WHERE c.participant1_id = ? OR c.participant2_id = ?"""
    count_query = "SELECT COUNT(*) as c FROM messages m JOIN conversations c ON m.conversation_id = c.id WHERE c.participant1_id = ? OR c.participant2_id = ?"
    params = (request.state.user_id, request.state.user_id)
    result = PaginationHelper.paginate_query(query, count_query, params, page, limit, "m.sent_at")
    return {"success": True, **result}


@router.post("/messages")
def send_message(request: Request):
    return {"success": True, "message": "Message sent"}


@router.get("/announcements")
def get_announcements(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    db = get_db()
    query = "SELECT title, content, priority, created_at FROM announcements WHERE expires_at IS NULL OR expires_at > datetime('now')"
    count_query = "SELECT COUNT(*) as c FROM announcements WHERE expires_at IS NULL OR expires_at > datetime('now')"
    result = PaginationHelper.paginate_query(query, count_query, (), page, limit)
    return {"success": True, **result}


@router.get("/events")
def get_events():
    """Get upcoming school events - shows active term dates"""
    db = get_db()
    rows = db.fetch_all("""
        SELECT 'Term ' || t.term_number as title, t.start_date || ' to ' || t.end_date as description, t.start_date
        FROM terms t JOIN academic_years ay ON t.academic_year_id = ay.id
        WHERE ay.is_current = 1 ORDER BY t.term_number
    """)
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}
