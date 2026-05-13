"""
Jinja SSS Platform - Input Sanitizer
Prevents XSS and SQL injection
"""

import re
import html


class InputSanitizer:
    @staticmethod
    def sanitize_string(value: str) -> str:
        if not value:
            return value
        value = html.escape(value, quote=True)
        value = value.replace('\x00', '')
        return ' '.join(value.split())

    @staticmethod
    def detect_xss(value: str) -> bool:
        patterns = [
            r"<script[^>]*>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>",
        ]
        for p in patterns:
            if re.search(p, value, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def detect_sql_injection(value: str) -> bool:
        patterns = [
            r"(\bUNION\b.*\bSELECT\b)",
            r"(\bDROP\b.*\bTABLE\b)",
            r"(--[^\n]*)",
            r"(;.*\bSELECT\b)",
        ]
        for p in patterns:
            if re.search(p, value, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        filename = filename.replace('\\', '/').split('/')[-1]
        filename = re.sub(r'[^\w\.\-]', '_', filename)
        filename = filename.lstrip('.')
        return filename[:255]
