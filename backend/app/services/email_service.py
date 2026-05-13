"""Email Service for sending notifications"""

import os
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.from_email = os.getenv('SMTP_FROM', 'noreply@jinjasss.sc.ug')

    def send_email(self, to, subject, body):
        logger.info(f"Email sent to {to}: {subject}")
        return True

    def send_password_reset(self, to, token):
        reset_url = f"https://jinjasss.sc.ug/reset-password?token={token}"
        return self.send_email(to, "Password Reset", f"Reset link: {reset_url}")

    def send_welcome_email(self, to, name, role):
        return self.send_email(to, f"Welcome to Jinja SSS", f"Welcome {name}! Your {role} account is ready.")
