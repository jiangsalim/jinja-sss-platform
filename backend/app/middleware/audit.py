"""Audit Middleware - logs all API requests"""

from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.audit import AuditLogger
import time


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        if hasattr(request.state, 'user_id') and request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            AuditLogger.log(
                user_id=request.state.user_id,
                action=f"{request.method}_{response.status_code}",
                resource=request.url.path,
                ip_address=request.client.host
            )
        return response
