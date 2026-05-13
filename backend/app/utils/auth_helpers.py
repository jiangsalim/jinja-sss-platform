"""Authentication Helpers - progressive delay and lockout"""

import time
from datetime import datetime, timedelta
from app.database import get_db


class AuthHelpers:
    @staticmethod
    def check_login_allowed(user_id: int = None, username: str = None) -> dict:
        """Check if login is allowed and return delay if needed"""
        db = get_db()
        if user_id:
            user = db.fetch_one("SELECT failed_attempts, locked_until FROM users WHERE id = ?", (user_id,))
        elif username:
            user = db.fetch_one("SELECT id, failed_attempts, locked_until FROM users WHERE username = ? OR email = ?", (username, username))
        else:
            return {"allowed": True, "delay": 0}

        if not user:
            return {"allowed": True, "delay": 0}

        if user['locked_until']:
            lock_time = datetime.fromisoformat(user['locked_until'])
            if datetime.utcnow() < lock_time:
                remaining = (lock_time - datetime.utcnow()).seconds
                return {"allowed": False, "delay": remaining, "locked": True}

        attempts = user['failed_attempts']
        if attempts >= 10:
            return {"allowed": False, "delay": 1800, "locked": True}
        elif attempts >= 6:
            delay = (attempts - 5) * 2
            return {"allowed": True, "delay": delay}
        return {"allowed": True, "delay": 0}

    @staticmethod
    def progressive_delay(attempts: int) -> int:
        """Calculate progressive delay based on failed attempts"""
        if attempts < 6: return 0
        return min((attempts - 5) * 2, 30)
