"""
Jinja SSS Platform - File Validator
Validates uploaded files
"""

import os


class FileValidator:
    ALLOWED_TYPES = {
        'image': {
            'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'mime_types': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
            'max_size': 5 * 1024 * 1024
        },
        'document': {
            'extensions': ['.pdf', '.doc', '.docx', '.xls', '.xlsx'],
            'mime_types': ['application/pdf'],
            'max_size': 10 * 1024 * 1024
        },
        'csv': {
            'extensions': ['.csv'],
            'mime_types': ['text/csv'],
            'max_size': 5 * 1024 * 1024
        }
    }

    @staticmethod
    def validate_extension(filename: str, file_type: str) -> bool:
        rules = FileValidator.ALLOWED_TYPES.get(file_type)
        if not rules:
            return False
        ext = os.path.splitext(filename)[1].lower()
        return ext in rules['extensions']

    @staticmethod
    def validate_size(file_size: int, file_type: str) -> bool:
        rules = FileValidator.ALLOWED_TYPES.get(file_type)
        if not rules:
            return False
        return file_size <= rules['max_size']
