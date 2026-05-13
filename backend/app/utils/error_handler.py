from fastapi import FastAPI, Request, HTTPException
from app.utils.response import error_response
from app.config import settings
import logging
logger = logging.getLogger(__name__)

def register_error_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
        return error_response(code=f"HTTP_{exc.status_code}", message=str(exc.detail), status_code=exc.status_code)
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        logger.warning(f"Validation error: {str(exc)}")
        return error_response(code="VALIDATION_ERROR", message=str(exc), status_code=400)
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        message = "An unexpected error occurred." if settings.APP_ENV == 'production' else str(exc)
        return error_response(code="INTERNAL_SERVER_ERROR", message=message, status_code=500)
