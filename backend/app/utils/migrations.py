"""
Jinja SSS Platform - Database Migration System
"""

import os
from app.database import get_db


class MigrationManager:
    @staticmethod
    def run_migrations():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        migrations_path = os.path.join(os.path.dirname(__file__), '../../database/migrations')
        if not os.path.exists(migrations_path):
            return
        applied = [r['name'] for r in db.fetch_all("SELECT name FROM migrations")]
        for f in sorted(os.listdir(migrations_path)):
            if f.endswith('.sql') and f not in applied:
                with open(os.path.join(migrations_path, f)) as sf:
                    db.execute(sf.read())
                db.execute("INSERT INTO migrations (name) VALUES (?)", (f,))
        return True
