"""HOD Dashboard API Routes"""

from fastapi import APIRouter, HTTPException, Request, Query
from app.database import get_db
from app.utils.pagination import PaginationHelper

router = APIRouter(prefix="/api/hod", tags=["HOD"])


def get_current_hod(request: Request):
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    db = get_db()
    teacher = db.fetch_one("SELECT * FROM teachers WHERE user_id = ?", (request.state.user_id,))
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher record not found")
    return dict(teacher)


@router.get("/dashboard")
def dashboard(request: Request):
    """HOD dashboard overview"""
    hod = get_current_hod(request)
    db = get_db()
    
    dept = db.fetch_one("SELECT * FROM departments WHERE id = ?", (hod['department_id'],))
    teachers = db.fetch_all("SELECT t.*, u.full_name FROM teachers t JOIN users u ON t.user_id = u.id WHERE t.department_id = ?", (hod['department_id'],))
    students = db.fetch_one("""
        SELECT COUNT(*) as c FROM students s JOIN classes c ON s.class_id = c.id
        JOIN teacher_subjects ts ON c.id = ts.class_id JOIN teachers t ON ts.teacher_id = t.id
        WHERE t.department_id = ?
    """, (hod['department_id'],))
    
    return {
        "success": True,
        "data": {
            "department": dict(dept) if dept else {},
            "teachers_count": len(teachers) if teachers else 0,
            "students_count": students['c'] if students else 0,
            "teachers": [dict(t) for t in teachers] if teachers else []
        }
    }


@router.get("/teachers")
def get_department_teachers(request: Request):
    hod = get_current_hod(request)
    db = get_db()
    teachers = db.fetch_all("""
        SELECT t.id, t.staff_id, t.teacher_type, t.qualification, u.full_name
        FROM teachers t JOIN users u ON t.user_id = u.id WHERE t.department_id = ?
    """, (hod['department_id'],))
    return {"success": True, "data": [dict(t) for t in teachers] if teachers else []}


@router.get("/lesson-plans/pending")
def get_pending_lesson_plans(request: Request):
    hod = get_current_hod(request)
    db = get_db()
    plans = db.fetch_all("""
        SELECT lp.*, u.full_name as teacher_name, s.name as subject_name
        FROM lesson_plans lp JOIN teachers t ON lp.teacher_id = t.id
        JOIN users u ON t.user_id = u.id JOIN subjects s ON lp.subject_id = s.id
        WHERE t.department_id = ? AND lp.status = 'pending'
        ORDER BY lp.submitted_at DESC
    """, (hod['department_id'],))
    return {"success": True, "data": [dict(p) for p in plans] if plans else []}


@router.post("/lesson-plans/{plan_id}/approve")
def approve_lesson_plan(plan_id: int, request: Request):
    hod = get_current_hod(request)
    db = get_db()
    db.execute("UPDATE lesson_plans SET status = 'approved', reviewed_by = ?, reviewed_at = datetime('now') WHERE id = ?", (hod['user_id'], plan_id))
    return {"success": True, "message": "Lesson plan approved"}


@router.get("/student-performance")
def get_student_performance(request: Request):
    hod = get_current_hod(request)
    db = get_db()
    performance = db.fetch_all("""
        SELECT s.name as subject, ROUND(AVG(g.score),1) as avg_score,
               COUNT(CASE WHEN g.score >= 50 THEN 1 END) as passed, COUNT(*) as total
        FROM grades g JOIN subjects s ON g.subject_id = s.id
        JOIN teacher_subjects ts ON g.subject_id = ts.subject_id
        JOIN teachers t ON ts.teacher_id = t.id
        WHERE t.department_id = ? GROUP BY s.name
    """, (hod['department_id'],))
    return {"success": True, "data": [dict(p) for p in performance] if performance else []}


@router.get("/class-allocation")
def get_class_allocation(request: Request):
    hod = get_current_hod(request)
    db = get_db()
    allocation = db.fetch_all("""
        SELECT c.name as class_name, u.full_name as teacher_name, s.name as subject_name
        FROM teacher_subjects ts JOIN classes c ON ts.class_id = c.id
        JOIN teachers t ON ts.teacher_id = t.id JOIN users u ON t.user_id = u.id
        JOIN subjects s ON ts.subject_id = s.id
        WHERE t.department_id = ? ORDER BY c.name, s.name
    """, (hod['department_id'],))
    return {"success": True, "data": [dict(a) for a in allocation] if allocation else []}


@router.get("/resources/pending")
def get_pending_resources(request: Request):
    return {"success": True, "data": []}


@router.get("/budget")
def get_department_budget(request: Request):
    hod = get_current_hod(request)
    db = get_db()
    dept = db.fetch_one("SELECT budget FROM departments WHERE id = ?", (hod['department_id'],))
    return {"success": True, "data": {"total_budget": dept['budget'] if dept else 0, "spent": 0, "remaining": dept['budget'] if dept else 0}}
