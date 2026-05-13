"""Session Manager - idle timeout, concurrent limits, revocation"""

from datetime import datetime, timedelta
from app.database import get_db


class SessionManager:
    IDLE_TIMEOUT_MINUTES = 15
    ABSOLUTE_TIMEOUT_HOURS = 8
    MAX_CONCURRENT_SESSIONS = 3

    @staticmethod
    def create_session(user_id: int, token: str, refresh_token: str = None, device_type: str = None, device_name: str = None, ip_address: str = None):
        db = get_db()
        now = datetime.utcnow()
        expires = now + timedelta(hours=SessionManager.ABSOLUTE_TIMEOUT_HOURS)
        db.execute("INSERT INTO sessions (user_id, token, refresh_token, device_type, device_name, ip_address, last_active, expires_at) VALUES (?,?,?,?,?,?,?,?)",
                   (user_id, token, refresh_token, device_type, device_name, ip_address, now.isoformat(), expires.isoformat()))
        SessionManager._enforce_limit(user_id)

    @staticmethod
    def _enforce_limit(user_id: int):
        db = get_db()
        sessions = db.fetch_all("SELECT id FROM sessions WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        if len(sessions) > SessionManager.MAX_CONCURRENT_SESSIONS:
            for s in sessions[SessionManager.MAX_CONCURRENT_SESSIONS:]:
                db.execute("DELETE FROM sessions WHERE id = ?", (s['id'],))

    @staticmethod
    def validate_session(user_id: int, token: str) -> bool:
        db = get_db()
        session = db.fetch_one("SELECT * FROM sessions WHERE user_id = ? AND token = ?", (user_id, token))
        if not session:
            return False
        now = datetime.utcnow()
        last_active = datetime.fromisoformat(session['last_active'])
        expires = datetime.fromisoformat(session['expires_at'])
        if now > expires:
            db.execute("DELETE FROM sessions WHERE id = ?", (session['id'],))
            return False
        idle_limit = last_active + timedelta(minutes=SessionManager.IDLE_TIMEOUT_MINUTES)
        if now > idle_limit:
            db.execute("DELETE FROM sessions WHERE id = ?", (session['id'],))
            return False
        db.execute("UPDATE sessions SET last_active = ? WHERE id = ?", (now.isoformat(), session['id']))
        return True

    @staticmethod
    def revoke_session(session_id: int):
        db = get_db()
        db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    @staticmethod
    def revoke_all_user_sessions(user_id: int, except_token: str = None):
        db = get_db()
        if except_token:
            db.execute("DELETE FROM sessions WHERE user_id = ? AND token != ?", (user_id, except_token))
        else:
            db.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))

    @staticmethod
    def get_active_sessions(user_id: int) -> list:
        db = get_db()
        return [dict(r) for r in db.fetch_all("SELECT id, device_type, device_name, ip_address, last_active, created_at FROM sessions WHERE user_id = ? ORDER BY last_active DESC", (user_id,))]

    @staticmethod
    def cleanup_expired_sessions():
        db = get_db()
        now = datetime.utcnow().isoformat()
        db.execute("DELETE FROM sessions WHERE expires_at < ?", (now,))
        db.execute("DELETE FROM sessions WHERE last_active < ?", 
                   ((datetime.utcnow() - timedelta(minutes=SessionManager.IDLE_TIMEOUT_MINUTES)).isoformat(),))
