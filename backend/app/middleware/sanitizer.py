"""Sanitization Middleware - sanitizes all incoming request data"""

from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.sanitizer import InputSanitizer
import json


class SanitizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method in ('POST', 'PUT', 'PATCH'):
            try:
                body = await request.body()
                if body:
                    data = json.loads(body)
                    sanitized = InputSanitizer.sanitize_dict(data)
                    request._body = json.dumps(sanitized).encode()
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        return await call_next(request)
