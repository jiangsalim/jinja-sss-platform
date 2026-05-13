"""
Jinja SSS Platform - Input Sanitizer
Prevents XSS, SQL Injection, and malicious input
"""

import re
import html


class InputSanitizer:
    @staticmethod
    def sanitize_string(value: str) -> str:
        if not value: return value
        value = html.escape(value, quote=True)
        value = value.replace('\x00', '')
        value = ' '.join(value.split())
        return value

    @staticmethod
    def sanitize_dict(data: dict) -> dict:
        if not data: return data
        return {k: InputSanitizer.sanitize_string(v) if isinstance(v, str) else v for k, v in data.items()}

    @staticmethod
    def detect_xss(value: str) -> bool:
        patterns = [
            r"<script[^>]*>", r"javascript:", r"on\w+\s*=", r"<iframe[^>]*>",
            r"<object[^>]*>", r"<embed[^>]*>", r"<link[^>]*>", r"expression\s*\(",
        ]
        for p in patterns:
            if re.search(p, value, re.IGNORECASE): return True
        return False

    @staticmethod
    def detect_sql_injection(value: str) -> bool:
        patterns = [
            r"(\bUNION\b.*\bSELECT\b)", r"(\bDROP\b.*\bTABLE\b)", r"(--[^\n]*)",
            r"(;.*\bSELECT\b)", r"(\bINSERT\b.*\bINTO\b)", r"(\bDELETE\b.*\bFROM\b)",
        ]
        for p in patterns:
            if re.search(p, value, re.IGNORECASE): return True
        return False

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        filename = filename.replace('\\', '/').split('/')[-1]
        filename = re.sub(r'[^\w\.\-]', '_', filename).lstrip('.')
        return filename[:255]

    @staticmethod
    def validate_sql_identifier(value: str) -> bool:
        return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value))
