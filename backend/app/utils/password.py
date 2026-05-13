import bcrypt
import secrets
import re
from datetime import datetime, timedelta
from app.database import get_db


class PasswordManager:
    MIN_LENGTH = 8
    STAFF_EXPIRY_DAYS = 90
    HISTORY_LIMIT = 5

    @staticmethod
    def hash_password(password: str) -> str:
        if not password or len(password) < PasswordManager.MIN_LENGTH:
            raise ValueError(f"Password must be at least {PasswordManager.MIN_LENGTH} characters")
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        if not password or not hashed:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False

    @staticmethod
    def check_password_strength(password: str) -> dict:
        score = 0
        feedback = []
        if len(password) >= PasswordManager.MIN_LENGTH:
            score += 1
        else:
            feedback.append(f"At least {PasswordManager.MIN_LENGTH} characters")
        if re.search(r'[A-Z]', password): score += 1
        else: feedback.append("Add an uppercase letter")
        if re.search(r'[a-z]', password): score += 1
        else: feedback.append("Add a lowercase letter")
        if re.search(r'\d', password): score += 1
        else: feedback.append("Add a number")
        if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password): score += 1
        else: feedback.append("Add a special character")
        strength = "weak" if score <= 2 else "medium" if score <= 3 else "strong" if score <= 4 else "very_strong"
        return {"score": score, "max_score": 5, "strength": strength, "feedback": feedback if feedback else ["Password is strong!"]}

    @staticmethod
    def check_password_history(user_id: int, new_password: str) -> bool:
        """Check if password was used in last 5 passwords"""
        db = get_db()
        history = db.fetch_all(
            "SELECT password_hash FROM password_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, PasswordManager.HISTORY_LIMIT)
        )
        for row in history:
            if PasswordManager.verify_password(new_password, row['password_hash']):
                return False
        return True

    @staticmethod
    def add_to_history(user_id: int, password_hash: str):
        db = get_db()
        db.execute("INSERT INTO password_history (user_id, password_hash) VALUES (?, ?)", (user_id, password_hash))
        count = db.fetch_one("SELECT COUNT(*) as c FROM password_history WHERE user_id = ?", (user_id,))
        if count and count['c'] > PasswordManager.HISTORY_LIMIT:
            db.execute("DELETE FROM password_history WHERE id IN (SELECT id FROM password_history WHERE user_id = ? ORDER BY created_at ASC LIMIT 1)", (user_id,))

    @staticmethod
    def is_password_expired(user_id: int) -> bool:
        db = get_db()
        user = db.fetch_one("SELECT role, password_changed_at FROM users WHERE id = ?", (user_id,))
        if not user:
            return False
        staff_roles = ['teacher', 'hod', 'admin', 'head_teacher', 'deputy_academics', 'deputy_welfare', 'registrar', 'director_studies', 'finance', 'hr']
        if user['role'] not in staff_roles:
            return False
        if not user['password_changed_at']:
            return True
        expiry = datetime.fromisoformat(user['password_changed_at']) + timedelta(days=PasswordManager.STAFF_EXPIRY_DAYS)
        return datetime.utcnow() > expiry

    @staticmethod
    def generate_temp_password() -> str:
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(secrets.choice(alphabet) for _ in range(12))
