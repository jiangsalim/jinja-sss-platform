"""Notifications Service for user alerts"""

import logging
from app.database import get_db

logger = logging.getLogger(__name__)


class NotificationsService:
    @staticmethod
    async def send(user_id, title, message, ntype='info'):
        db = get_db()
        db.execute("INSERT INTO notifications (user_id, title, message, type) VALUES (?,?,?,?)", (user_id, title, message, ntype))
        logger.info(f"Notification sent to user {user_id}")

    @staticmethod
    async def broadcast(title, message, roles=None):
        db = get_db()
        if roles:
            for role in roles:
                users = db.fetch_all("SELECT id FROM users WHERE role = ? AND is_active = 1", (role,))
                for u in users:
                    await NotificationsService.send(u['id'], title, message, 'important')
        logger.info(f"Broadcast sent: {title}")
