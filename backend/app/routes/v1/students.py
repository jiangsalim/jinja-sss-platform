"""Student Dashboard API Routes"""

from fastapi import APIRouter, HTTPException, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper
from datetime import datetime

router = APIRouter(prefix="/api/student", tags=["Student"])


def get_current_student(request: Request):
    """Get the student record for the logged-in user"""
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    db = get_db()
    student = db.fetch_one("SELECT * FROM students WHERE user_id = ?", (request.state.user_id,))
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")
    return dict(student)


@router.get("/dashboard")
def dashboard(request: Request):
    """Student dashboard overview"""
    student = get_current_student(request)
    db = get_db()
    student_id = student['id']
    
    # Attendance stats
    total_days = db.fetch_one("SELECT COUNT(*) as c FROM attendance WHERE student_id = ?", (student_id,))
    present_days = db.fetch_one("SELECT COUNT(*) as c FROM attendance WHERE student_id = ? AND status = 'present'", (student_id,))
    attendance_pct = round((present_days['c'] / total_days['c']) * 100) if total_days and total_days['c'] > 0 else 0
    
    # Grade stats
    avg_grade = db.fetch_one("SELECT AVG(score) as avg FROM grades WHERE student_id = ?", (student_id,))
    
    # Timetable
    timetable = db.fetch_all("""
        SELECT t.day_of_week, t.start_time, t.end_time, s.name as subject, u.full_name as teacher, t.room
        FROM timetable t JOIN subjects s ON t.subject_id = s.id JOIN teachers te ON t.teacher_id = te.id JOIN users u ON te.user_id = u.id
        WHERE t.class_id = ? AND t.stream_id = ? ORDER BY t.day_of_week, t.start_time
    """, (student['class_id'], student['stream_id']))
    
    # Pending assignments
    assignments = db.fetch_all("""
        SELECT h.id, h.title, h.due_date, s.name as subject
        FROM homework h JOIN subjects s ON h.subject_id = s.id
        WHERE h.class_id = ? AND h.id NOT IN (SELECT homework_id FROM homework_submissions WHERE student_id = ?)
        ORDER BY h.due_date ASC
    """, (student['class_id'], student_id))
    
    # Recent grades
    grades = db.fetch_all("""
        SELECT g.score, g.grade, s.name as subject, g.exam_type
        FROM grades g JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = ? ORDER BY g.recorded_at DESC LIMIT 6
    """, (student_id,))
    
    return {
        "success": True,
        "data": {
            "student": {"id": student['id'], "admission_number": student['admission_number'], "class": student['class_id']},
            "stats": {"attendance": attendance_pct, "average_grade": round(avg_grade['avg'], 1) if avg_grade['avg'] else 0, "exams_soon": 0, "pending_work": len(assignments)},
            "timetable": [dict(t) for t in timetable] if timetable else [],
            "assignments": [dict(a) for a in assignments] if assignments else [],
            "grades": [dict(g) for g in grades] if grades else []
        }
    }


@router.get("/grades")
def get_grades(request: Request, term_id: int = None, subject_id: int = None, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    """Get student grades with filters"""
    student = get_current_student(request)
    db = get_db()
    
    query = "SELECT g.*, s.name as subject_name FROM grades g JOIN subjects s ON g.subject_id = s.id WHERE g.student_id = ?"
    count_query = "SELECT COUNT(*) as c FROM grades WHERE student_id = ?"
    params = [student['id']]
    
    if term_id:
        query += " AND g.term_id = ?"
        count_query += " AND term_id = ?"
        params.append(term_id)
    if subject_id:
        query += " AND g.subject_id = ?"
        count_query += " AND subject_id = ?"
        params.append(subject_id)
    
    result = PaginationHelper.paginate_query(query, count_query, tuple(params), page, limit, "g.recorded_at")
    return {"success": True, **result}


@router.get("/attendance")
def get_attendance(request: Request, term_id: int = None, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    """Get student attendance history"""
    student = get_current_student(request)
    db = get_db()
    
    query = "SELECT date, status, period FROM attendance WHERE student_id = ?"
    count_query = "SELECT COUNT(*) as c FROM attendance WHERE student_id = ?"
    params = [student['id']]
    
    result = PaginationHelper.paginate_query(query, count_query, tuple(params), page, limit, "date")
    return {"success": True, **result}


@router.get("/timetable")
def get_timetable(request: Request):
    """Get student weekly timetable"""
    student = get_current_student(request)
    db = get_db()
    rows = db.fetch_all("""
        SELECT t.day_of_week, t.start_time, t.end_time, s.name as subject, u.full_name as teacher, t.room
        FROM timetable t JOIN subjects s ON t.subject_id = s.id JOIN teachers te ON t.teacher_id = te.id JOIN users u ON te.user_id = u.id
        WHERE t.class_id = ? AND t.stream_id = ? ORDER BY t.day_of_week, t.start_time
    """, (student['class_id'], student['stream_id']))
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.get("/assignments")
def get_assignments(request: Request):
    """Get pending assignments"""
    student = get_current_student(request)
    db = get_db()
    rows = db.fetch_all("""
        SELECT h.id, h.title, h.description, h.due_date, s.name as subject
        FROM homework h JOIN subjects s ON h.subject_id = s.id
        WHERE h.class_id = ? AND h.id NOT IN (SELECT homework_id FROM homework_submissions WHERE student_id = ?)
        ORDER BY h.due_date ASC
    """, (student['class_id'], student['id']))
    return {"success": True, "data": [dict(r) for r in rows] if rows else []}


@router.post("/assignments/{assignment_id}/submit")
def submit_assignment(assignment_id: int, request: Request):
    """Submit an assignment"""
    student = get_current_student(request)
    db = get_db()
    db.execute("INSERT INTO homework_submissions (homework_id, student_id, submission_date, status) VALUES (?,?,?,?)",
               (assignment_id, student['id'], datetime.utcnow().isoformat(), 'submitted'))
    return {"success": True, "message": "Assignment submitted"}


@router.get("/messages")
def get_messages(request: Request, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    """Get student messages"""
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    db = get_db()
    query = """SELECT c.id as conversation_id, u.full_name as sender, m.message, m.sent_at, m.is_read
               FROM messages m JOIN conversations c ON m.conversation_id = c.id JOIN users u ON m.sender_id = u.id
               WHERE c.participant1_id = ? OR c.participant2_id = ?"""
    count_query = """SELECT COUNT(*) as c FROM messages m JOIN conversations c ON m.conversation_id = c.id
                     WHERE c.participant1_id = ? OR c.participant2_id = ?"""
    params = (request.state.user_id, request.state.user_id)
    result = PaginationHelper.paginate_query(query, count_query, params, page, limit, "m.sent_at")
    return {"success": True, **result}


@router.post("/messages")
def send_message(request: Request):
    """Send a message"""
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    return {"success": True, "message": "Message sent"}


@router.get("/announcements")
def get_announcements(request: Request, page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    """Get school announcements"""
    db = get_db()
    query = "SELECT title, content, priority, created_at FROM announcements WHERE expires_at IS NULL OR expires_at > datetime('now')"
    count_query = "SELECT COUNT(*) as c FROM announcements WHERE expires_at IS NULL OR expires_at > datetime('now')"
    result = PaginationHelper.paginate_query(query, count_query, (), page, limit)
    return {"success": True, **result}
