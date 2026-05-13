"""Database Backup Service"""

import os
import shutil
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class BackupService:
    def __init__(self):
        self.backup_path = os.getenv('BACKUP_PATH', './backups')
        self.db_path = os.getenv('DATABASE_PATH', './database/school.db')
        os.makedirs(self.backup_path, exist_ok=True)

    def create_backup(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"school_backup_{timestamp}.db"
        filepath = os.path.join(self.backup_path, filename)
        shutil.copy2(self.db_path, filepath)
        logger.info(f"Backup created: {filename}")
        return filename

    def list_backups(self):
        backups = []
        for f in os.listdir(self.backup_path):
            if f.endswith('.db'):
                path = os.path.join(self.backup_path, f)
                backups.append({'name': f, 'size': os.path.getsize(path), 'created': datetime.fromtimestamp(os.path.getctime(path)).isoformat()})
        return sorted(backups, key=lambda x: x['created'], reverse=True)
