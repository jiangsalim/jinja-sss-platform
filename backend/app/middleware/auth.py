"""Authentication Middleware - validates JWT on every request"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth import TokenManager


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public = ['/health', '/docs', '/openapi.json', '/redoc', '/auth/signin', '/auth/signup', '/', '/api/docs', '/api/redoc', '/api/openapi.json']
        if any(request.url.path.startswith(p) for p in public):
            return await call_next(request)
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        token = auth.split(' ')[1]
        payload = TokenManager.decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        request.state.user_id = payload.get('user_id')
        request.state.role = payload.get('role')
        return await call_next(request)
