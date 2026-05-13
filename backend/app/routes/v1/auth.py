"""Authentication Routes - Signup, Signin, Password Management"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.auth import TokenManager
from app.utils.password import PasswordManager
from app.utils.session_manager import SessionManager
from app.utils.audit import AuditLogger
from app.utils.auth_helpers import AuthHelpers
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])


class SigninRequest(BaseModel):
    identifier: str
    password: str


class SignupRequest(BaseModel):
    full_name: str
    email: str = None
    phone: str = None
    username: str = None
    password: str
    role: str = "parent"


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


@router.post("/signin")
def signin(request: Request, data: SigninRequest):
    db = get_db()
    
    # Find user by username, email, or admission number
    user = db.fetch_one(
        "SELECT * FROM users WHERE username = ? OR email = ? OR id = (SELECT user_id FROM students WHERE admission_number = ?) OR id = (SELECT user_id FROM teachers WHERE staff_id = ?)",
        (data.identifier, data.identifier, data.identifier, data.identifier)
    )
    
    if not user:
        AuditLogger.log(None, 'LOGIN_FAILED', ip_address=request.client.host)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check account lockout
    lockout = AuthHelpers.check_login_allowed(user_id=user['id'])
    if not lockout['allowed']:
        raise HTTPException(status_code=423, detail=f"Account locked. Try again in {lockout['delay']} seconds")
    
    # Verify password
    if not PasswordManager.verify_password(data.password, user['password_hash']):
        PasswordManager.record_failed_attempt(user['id'])
        AuditLogger.log_login(user['id'], False, request.client.host)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Reset failed attempts
    PasswordManager.reset_failed_attempts(user['id'])
    
    # Check password expiry
    if PasswordManager.is_password_expired(user['id']):
        tokens = TokenManager.create_token_pair(user['id'], user['username'], user['role'], True)
        return {"success": True, "first_login": True, "message": "Password expired. Please change.", **tokens}
    
    # Create session
    tokens = TokenManager.create_token_pair(user['id'], user['username'], user['role'], user['first_login'])
    SessionManager.create_session(user['id'], tokens['access_token'], tokens['refresh_token'], 
                                   request.headers.get('User-Agent', 'unknown'), request.client.host)
    AuditLogger.log_login(user['id'], True, request.client.host)
    
    # Update last login
    db.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.utcnow().isoformat(), user['id']))
    
    return {
        "success": True,
        "message": "Login successful",
        "user": {"id": user['id'], "username": user['username'], "full_name": user['full_name'], "role": user['role']},
        **tokens
    }


@router.post("/signup")
def signup(data: SignupRequest):
    db = get_db()
    
    # Validate password strength
    strength = PasswordManager.check_password_strength(data.password)
    if strength['score'] < 3:
        raise HTTPException(status_code=400, detail=f"Weak password: {', '.join(strength['feedback'])}")
    
    # Check existing user
    existing = db.fetch_one("SELECT id FROM users WHERE username = ? OR email = ?", (data.username, data.email))
    if existing:
        raise HTTPException(status_code=409, detail="Username or email already exists")
    
    # Create user
    password_hash = PasswordManager.hash_password(data.password)
    db.execute(
        "INSERT INTO users (username, email, full_name, role, phone, password_hash) VALUES (?,?,?,?,?,?)",
        (data.username, data.email, data.full_name, data.role, data.phone, password_hash)
    )
    user_id = db.fetch_one("SELECT last_insert_rowid() as id")['id']
    
    # Add to password history
    PasswordManager.add_to_history(user_id, password_hash)
    
    AuditLogger.log(user_id, 'USER_CREATE', 'users', user_id)
    
    return {"success": True, "message": "Account created successfully. Please sign in.", "user_id": user_id}


@router.post("/change-password")
def change_password(request: Request, data: PasswordChangeRequest):
    if not hasattr(request.state, 'user_id'):
        raise HTTPException(status_code=401)
    
    db = get_db()
    user = db.fetch_one("SELECT * FROM users WHERE id = ?", (request.state.user_id,))
    
    if not PasswordManager.verify_password(data.current_password, user['password_hash']):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Check new password strength
    strength = PasswordManager.check_password_strength(data.new_password)
    if strength['score'] < 3:
        raise HTTPException(status_code=400, detail=f"Weak password: {', '.join(strength['feedback'])}")
    
    # Check password history
    if not PasswordManager.check_password_history(request.state.user_id, data.new_password):
        raise HTTPException(status_code=400, detail="Password was used recently. Choose a different one.")
    
    # Update password
    new_hash = PasswordManager.hash_password(data.new_password)
    db.execute("UPDATE users SET password_hash = ?, password_changed_at = ?, first_login = 0 WHERE id = ?",
               (new_hash, datetime.utcnow().isoformat(), request.state.user_id))
    PasswordManager.add_to_history(request.state.user_id, new_hash)
    
    AuditLogger.log_password_change(request.state.user_id)
    
    return {"success": True, "message": "Password changed successfully"}


@router.post("/reset-password/request")
def request_reset(data: PasswordResetRequest):
    # In production, send email with reset link
    return {"success": True, "message": "If the email exists, a reset link has been sent."}


@router.post("/reset-password/confirm")
def confirm_reset(data: PasswordResetConfirm):
    # In production, validate token and update password
    return {"success": True, "message": "Password reset successful. Please login."}


@router.post("/refresh")
def refresh_token(request: Request):
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        raise HTTPException(status_code=401)
    
    token = auth.split(' ')[1]
    payload = TokenManager.decode_token(token)
    if not payload or payload.get('type') != 'refresh':
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = get_db().fetch_one("SELECT * FROM users WHERE id = ?", (payload['user_id'],))
    if not user:
        raise HTTPException(status_code=401)
    
    new_tokens = TokenManager.create_token_pair(user['id'], user['username'], user['role'])
    return {"success": True, **new_tokens}
