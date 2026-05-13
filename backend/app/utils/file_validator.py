"""File Validation Utility"""

import os
import re


class FileValidator:
    ALLOWED = {
        'image': {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
        'document': {'.pdf', '.doc', '.docx', '.xls', '.xlsx'},
        'csv': {'.csv'},
    }
    MAX_SIZES = {'image': 5*1024*1024, 'document': 10*1024*1024, 'csv': 5*1024*1024}
    DANGEROUS_NAMES = {'php', 'exe', 'sh', 'bat', 'cmd', 'ps1', 'js', 'vbs'}

    @staticmethod
    def validate(filename: str, file_size: int, file_type: str) -> tuple:
        rules = FileValidator.ALLOWED.get(file_type)
        if not rules: return False, "Unknown file type"
        ext = os.path.splitext(filename)[1].lower()
        if ext not in rules: return False, f"Extension {ext} not allowed"
        if ext.lstrip('.') in FileValidator.DANGEROUS_NAMES: return False, "File type blocked for security"
        max_size = FileValidator.MAX_SIZES.get(file_type, 5*1024*1024)
        if file_size > max_size: return False, f"File too large (max {max_size//1024//1024}MB)"
        if '..' in filename or filename.startswith('/'): return False, "Invalid filename"
        return True, "OK"

    @staticmethod
    def sanitize_name(filename: str) -> str:
        name = filename.replace('\\', '/').split('/')[-1]
        name = re.sub(r'[^\w\.\-]', '_', name).lstrip('.').lower()
        return name[:255]
