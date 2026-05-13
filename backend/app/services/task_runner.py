"""Background Task Runner for async operations"""

import asyncio
import logging

logger = logging.getLogger(__name__)


class TaskRunner:
    @staticmethod
    async def run(func, *args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Background task failed: {e}")

    @staticmethod
    async def send_email_background(to, subject, body):
        logger.info(f"Email queued: {to} - {subject}")

    @staticmethod
    async def create_backup_background():
        logger.info("Backup task queued")
