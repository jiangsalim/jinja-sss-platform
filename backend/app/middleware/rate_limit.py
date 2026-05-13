"""Rate Limiting Middleware - prevents abuse per endpoint type"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)
        self.limits = {
            'auth': (5, 900),
            'api': (100, 60),
            'bulk': (10, 60),
            'upload': (20, 300),
        }

    def get_category(self, path: str) -> str:
        if path.startswith('/auth'):
            return 'auth'
        if 'bulk' in path or 'import' in path:
            return 'bulk'
        if path.startswith('/upload'):
            return 'upload'
        return 'api'

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        category = self.get_category(request.url.path)
        limit, window = self.limits.get(category, (100, 60))
        now = time.time()
        self.requests[ip] = [t for t in self.requests[ip] if now - t < window]
        if len(self.requests[ip]) >= limit:
            raise HTTPException(status_code=429, detail=f"Too many requests. Limit: {limit} per {window}s")
        self.requests[ip].append(now)
        response = await call_next(request)
        response.headers['X-RateLimit-Limit'] = str(limit)
        response.headers['X-RateLimit-Remaining'] = str(limit - len(self.requests[ip]))
        return response
