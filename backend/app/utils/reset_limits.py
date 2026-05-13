"""Password Reset Rate Limiting"""

from collections import defaultdict
import time


class ResetLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.max_requests = 3
        self.window = 3600

    def is_allowed(self, email: str) -> bool:
        now = time.time()
        self.requests[email] = [t for t in self.requests[email] if now - t < self.window]
        if len(self.requests[email]) >= self.max_requests:
            return False
        self.requests[email].append(now)
        return True

    def remaining(self, email: str) -> int:
        now = time.time()
        self.requests[email] = [t for t in self.requests[email] if now - t < self.window]
        return max(0, self.max_requests - len(self.requests[email]))


reset_limiter = ResetLimiter()
