"""Audit Logging Utility - tracks all sensitive actions"""

from app.database import get_db
from datetime import datetime
import json


class AuditLogger:
    @staticmethod
    def log(user_id: int, action: str, resource: str = None, resource_id: int = None,
            old_value=None, new_value=None, ip_address: str = None, user_agent: str = None):
        db = get_db()
        db.execute("""
            INSERT INTO audit_log (user_id, action, resource, resource_id, old_value, new_value, ip_address, user_agent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, action, resource, resource_id,
            json.dumps(old_value) if old_value else None,
            json.dumps(new_value) if new_value else None,
            ip_address, user_agent, datetime.utcnow().isoformat()
        ))

    @staticmethod
    def log_login(user_id: int, success: bool, ip: str = None):
        AuditLogger.log(user_id, 'LOGIN_SUCCESS' if success else 'LOGIN_FAILED', 'auth', user_id, ip_address=ip)

    @staticmethod
    def log_logout(user_id: int):
        AuditLogger.log(user_id, 'LOGOUT', 'auth', user_id)

    @staticmethod
    def log_password_change(user_id: int):
        AuditLogger.log(user_id, 'PASSWORD_CHANGE', 'auth', user_id)

    @staticmethod
    def log_grade_change(user_id: int, grade_id: int, old_score: float, new_score: float):
        AuditLogger.log(user_id, 'GRADE_UPDATE', 'grades', grade_id, {'score': old_score}, {'score': new_score})

    @staticmethod
    def log_user_create(admin_id: int, new_user_id: int):
        AuditLogger.log(admin_id, 'USER_CREATE', 'users', new_user_id)

    @staticmethod
    def log_user_delete(admin_id: int, deleted_user_id: int):
        AuditLogger.log(admin_id, 'USER_DELETE', 'users', deleted_user_id)

    @staticmethod
    def log_fee_payment(user_id: int, payment_id: int, amount: float):
        AuditLogger.log(user_id, 'PAYMENT_CREATE', 'fees', payment_id, new_value={'amount': amount})
