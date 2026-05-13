import bcrypt
import secrets
import re

class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
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
        if len(password) >= 8: score += 1
        else: feedback.append("At least 8 characters")
        if re.search(r'[A-Z]', password): score += 1
        else: feedback.append("Add an uppercase letter")
        if re.search(r'[a-z]', password): score += 1
        else: feedback.append("Add a lowercase letter")
        if re.search(r'\d', password): score += 1
        else: feedback.append("Add a number")
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 1
        else: feedback.append("Add a special character")
        strength = "weak" if score <= 2 else "medium" if score <= 3 else "strong" if score <= 4 else "very_strong"
        return {"score": score, "max_score": 5, "strength": strength, "feedback": feedback if feedback else ["Password is strong!"]}

    @staticmethod
    def generate_temp_password() -> str:
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(secrets.choice(alphabet) for _ in range(12))
