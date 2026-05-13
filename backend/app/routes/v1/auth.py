"""Authentication Routes"""

from fastapi import APIRouter, HTTPException, Request
from app.auth import TokenManager
from app.utils.password import PasswordManager
from app.utils.session_manager import SessionManager
from app.utils.audit import AuditLogger
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signin")
def signin(request: Request):
    return {"message": "Signin endpoint ready for implementation"}


@router.post("/signup")
def signup():
    return {"message": "Signup endpoint ready for implementation"}


@router.get("/sessions")
def get_sessions(request: Request):
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    return {"sessions": SessionManager.get_active_sessions(request.state.user_id)}


@router.delete("/sessions/{session_id}")
def revoke_session(session_id: int, request: Request):
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    SessionManager.revoke_session(session_id)
    AuditLogger.log(request.state.user_id, 'SESSION_REVOKE', 'sessions', session_id)
    return {"success": True, "message": "Session revoked"}


@router.post("/logout")
def logout(request: Request):
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    SessionManager.revoke_all_user_sessions(request.state.user_id, token)
    AuditLogger.log_logout(request.state.user_id)
    return {"success": True, "message": "Logged out successfully"}
