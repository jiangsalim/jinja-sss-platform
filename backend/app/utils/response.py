from datetime import datetime
from fastapi.responses import JSONResponse

def success_response(data=None, message="Success", status_code=200):
    return JSONResponse(content={"success": True, "message": message, "data": data, "timestamp": datetime.utcnow().isoformat()}, status_code=status_code)

def error_response(code, message, details=None, status_code=400):
    return JSONResponse(content={"success": False, "error": {"code": code, "message": message, "details": details or {}}, "timestamp": datetime.utcnow().isoformat()}, status_code=status_code)

def paginated_response(data, pagination, filters=None):
    return {"success": True, "data": data, "pagination": pagination, "active_filters": filters or {}, "timestamp": datetime.utcnow().isoformat()}
