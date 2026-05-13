"""Rate Limiting Middleware"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time, os


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting if disabled
        if os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'false':
            return await call_next(request)
        
        ip = request.client.host
        now = time.time()
        self.requests[ip] = [t for t in self.requests[ip] if now - t < 60]
        if len(self.requests[ip]) >= 100:
            raise HTTPException(status_code=429, detail="Too many requests")
        self.requests[ip].append(now)
        return await call_next(request)
