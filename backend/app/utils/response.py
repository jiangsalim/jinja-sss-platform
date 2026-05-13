from datetime import datetime
from fastapi.responses import JSONResponse

def success_response(data=None, message="Success", status_code=200):
    return JSONResponse(content={"success": True, "message": message, "data": data, "timestamp": datetime.utcnow().isoformat()}, status_code=status_code)

def error_response(code, message, details=None, status_code=400):
    return JSONResponse(content={"success": False, "error": {"code": code, "message": message, "details": details or {}}, "timestamp": datetime.utcnow().isoformat()}, status_code=status_code)

def paginated_response(data, pagination, filters=None):
    return {"success": True, "data": data, "pagination": pagination, "active_filters": filters or {}, "timestamp": datetime.utcnow().isoformat()}

def rate_limit_response(data, limit, remaining, reset_time):
    """Create response with rate limit headers"""
    from fastapi.responses import JSONResponse
    response = JSONResponse(content={"success": True, "data": data})
    response.headers['X-RateLimit-Limit'] = str(limit)
    response.headers['X-RateLimit-Remaining'] = str(remaining)
    response.headers['X-RateLimit-Reset'] = str(reset_time)
    return response
