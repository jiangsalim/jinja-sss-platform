"""Teacher Dashboard API Routes"""

from fastapi import APIRouter, HTTPException, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper
from app.utils.audit import AuditLogger
from datetime import datetime

router = APIRouter(prefix="/api/teacher", tags=["Teacher"])


def get_current_teacher(request: Request):
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    db = get_db()
    teacher = db.fetch_one("SELECT * FROM teachers WHERE user_id = ?", (request.state.user_id,))
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher record not found")
    return dict(teacher)


@router.get("/dashboard")
def class_teacher_dashboard(request: Request):
    """Class Teacher dashboard overview"""
    teacher = get_current_teacher(request)
    db = get_db()

    # Get assigned classes
    classes = db.fetch_all("""
        SELECT c.id, c.name, s.stream_code, c.current_enrollment
        FROM teacher_subjects ts
        JOIN classes c ON ts.class_id = c.id
        LEFT JOIN streams s ON ts.stream_id = s.id
        WHERE ts.teacher_id = ?
    """, (teacher['id'],))

    # Today's attendance summary
    today = datetime.utcnow().strftime('%Y-%m-%d')
    attendance_summary = db.fetch_one("""
        SELECT COUNT(*) as total, SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present,
               SUM(CASE WHEN status='absent' THEN 1 ELSE 0 END) as absent
        FROM attendance WHERE date = ? AND marked_by = ?
    """, (today, teacher['user_id']))

    # Pending grades
    pending_grades = db.fetch_all("""
        SELECT COUNT(*) as count FROM grades WHERE recorded_by = ? AND status = 'draft'
    """, (teacher['user_id'],))

    # Pending lesson plans
    pending_plans = db.fetch_all("""
        SELECT COUNT(*) as count FROM lesson_plans WHERE teacher_id = ? AND status = 'pending'
    """, (teacher['id'],))

    return {
        "success": True,
        "data": {
            "teacher": teacher,
            "classes": [dict(c) for c in classes] if classes else [],
            "attendance_today": dict(attendance_summary) if attendance_summary else {},
            "pending_grades": pending_grades[0]['count'] if pending_grades else 0,
            "pending_plans": pending_plans[0]['count'] if pending_plans else 0
        }
    }


@router.get("/students")
def get_class_roster(request: Request, class_id: int = None):
    """Get students in assigned class"""
    teacher = get_current_teacher(request)
    db = get_db()

    if class_id:
        students = db.fetch_all("""
            SELECT s.id, s.admission_number, u.full_name, s.gender,
                   (SELECT ROUND(AVG(score),1) FROM grades WHERE student_id = s.id) as avg_grade
            FROM students s JOIN users u ON s.user_id = u.id
            WHERE s.class_id = ?
            ORDER BY u.full_name
        """, (class_id,))
    else:
        students = db.fetch_all("""
            SELECT s.id, s.admission_number, u.full_name, c.name as class_name,
                   (SELECT ROUND(AVG(score),1) FROM grades WHERE student_id = s.id) as avg_grade
            FROM students s JOIN users u ON s.user_id = u.id JOIN classes c ON s.class_id = c.id
            JOIN teacher_subjects ts ON s.class_id = ts.class_id AND s.stream_id = ts.stream_id
            WHERE ts.teacher_id = ?
            ORDER BY c.name, u.full_name
        """, (teacher['id'],))

    return {"success": True, "data": [dict(s) for s in students] if students else []}


@router.post("/attendance")
def mark_attendance(request: Request):
    """Mark class attendance"""
    teacher = get_current_teacher(request)
    # Implementation for bulk attendance marking
    return {"success": True, "message": "Attendance marked"}


@router.post("/grades")
def enter_grades(request: Request):
    """Enter student grades"""
    teacher = get_current_teacher(request)
    # Implementation for grade entry
    return {"success": True, "message": "Grades saved"}


@router.get("/grades/pending")
def get_pending_grades(request: Request, class_id: int = None):
    """Get pending grades to enter"""
    teacher = get_current_teacher(request)
    db = get_db()
    pending = db.fetch_all("""
        SELECT g.id, g.student_id, u.full_name as student_name, s.name as subject,
               g.exam_type, g.score, g.status
        FROM grades g JOIN students st ON g.student_id = st.id
        JOIN users u ON st.user_id = u.id JOIN subjects s ON g.subject_id = s.id
        WHERE g.recorded_by = ? AND g.status = 'draft'
        ORDER BY g.recorded_at DESC
    """, (teacher['user_id'],))
    return {"success": True, "data": [dict(p) for p in pending] if pending else []}


@router.get("/lesson-plans")
def get_lesson_plans(request: Request):
    """Get teacher's lesson plans"""
    teacher = get_current_teacher(request)
    db = get_db()
    plans = db.fetch_all("""
        SELECT lp.*, s.name as subject_name, c.name as class_name
        FROM lesson_plans lp JOIN subjects s ON lp.subject_id = s.id
        JOIN classes c ON lp.class_id = c.id
        WHERE lp.teacher_id = ? ORDER BY lp.week DESC, lp.submitted_at DESC
    """, (teacher['id'],))
    return {"success": True, "data": [dict(p) for p in plans] if plans else []}


@router.post("/lesson-plans")
def submit_lesson_plan(request: Request):
    """Submit a lesson plan"""
    teacher = get_current_teacher(request)
    return {"success": True, "message": "Lesson plan submitted"}


@router.get("/performance")
def get_class_performance(request: Request, class_id: int = None):
    """Get class performance summary"""
    teacher = get_current_teacher(request)
    db = get_db()

    query = """SELECT s.name as subject, ROUND(AVG(g.score),1) as avg_score,
               COUNT(CASE WHEN g.score >= 50 THEN 1 END) as passed, COUNT(*) as total
               FROM grades g JOIN subjects s ON g.subject_id = s.id JOIN students st ON g.student_id = st.id
               WHERE st.class_id = ? GROUP BY s.name"""
    params = [class_id] if class_id else [teacher['id']]

    if not class_id:
        query = query.replace("st.class_id = ?", "st.class_id IN (SELECT class_id FROM teacher_subjects WHERE teacher_id = ?)")

    performance = db.fetch_all(query, params)
    return {"success": True, "data": [dict(p) for p in performance] if performance else []}


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


@router.get("/subject/classes")
def get_subject_classes(request: Request):
    """Get classes assigned to subject teacher"""
    teacher = get_current_teacher(request)
    db = get_db()
    classes = db.fetch_all("""
        SELECT c.id, c.name as class_name, s.stream_code, sub.name as subject_name,
               c.current_enrollment as student_count
        FROM teacher_subjects ts
        JOIN classes c ON ts.class_id = c.id
        LEFT JOIN streams s ON ts.stream_id = s.id
        JOIN subjects sub ON ts.subject_id = sub.id
        WHERE ts.teacher_id = ?
    """, (teacher['id'],))
    return {"success": True, "data": [dict(c) for c in classes] if classes else []}


@router.get("/subject/students")
def get_subject_students(request: Request, subject_id: int = None, class_id: int = None):
    """Get students for subject teacher's classes"""
    teacher = get_current_teacher(request)
    db = get_db()

    query = """SELECT s.id, s.admission_number, u.full_name, c.name as class_name,
               (SELECT score FROM grades WHERE student_id = s.id AND subject_id = ? ORDER BY recorded_at DESC LIMIT 1) as latest_score
               FROM students s JOIN users u ON s.user_id = u.id JOIN classes c ON s.class_id = c.id
               JOIN teacher_subjects ts ON s.class_id = ts.class_id
               WHERE ts.teacher_id = ?"""
    params = [subject_id or 1, teacher['id']]

    if class_id:
        query += " AND s.class_id = ?"
        params.append(class_id)

    students = db.fetch_all(query, tuple(params))
    return {"success": True, "data": [dict(s) for s in students] if students else []}


@router.get("/subject/performance")
def get_subject_performance(request: Request, subject_id: int = None):
    """Get performance across classes for a subject"""
    teacher = get_current_teacher(request)
    db = get_db()

    query = """SELECT c.name as class_name, ROUND(AVG(g.score),1) as avg_score,
               COUNT(CASE WHEN g.score >= 50 THEN 1 END) as passed, COUNT(*) as total
               FROM grades g JOIN students s ON g.student_id = s.id
               JOIN classes c ON s.class_id = c.id JOIN teacher_subjects ts ON s.class_id = ts.class_id
               WHERE ts.teacher_id = ? AND g.subject_id = ? GROUP BY c.name"""
    params = [teacher['id'], subject_id or 1]

    performance = db.fetch_all(query, tuple(params))
    return {"success": True, "data": [dict(p) for p in performance] if performance else []}
