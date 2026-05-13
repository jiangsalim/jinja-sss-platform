from jose import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.config import settings


class TokenManager:
    @staticmethod
    def create_access_token(user_id: int, username: str, role: str, first_login: bool = False) -> str:
        payload = {
            "sub": username,
            "user_id": user_id,
            "role": role,
            "first_login": first_login,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(user_id: int, username: str) -> str:
        payload = {
            "sub": username,
            "user_id": user_id,
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def create_token_pair(user_id: int, username: str, role: str, first_login: bool = False) -> dict:
        return {
            "access_token": TokenManager.create_access_token(user_id, username, role, first_login),
            "refresh_token": TokenManager.create_refresh_token(user_id, username),
            "token_type": "bearer",
            "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "first_login": first_login
        }
