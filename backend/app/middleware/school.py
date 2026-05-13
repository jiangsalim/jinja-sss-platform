"""School Context Middleware - multi-tenant support"""

from starlette.middleware.base import BaseHTTPMiddleware


class SchoolContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        school_id = request.headers.get('X-School-ID')
        if school_id:
            request.state.school_id = school_id
        return await call_next(request)
