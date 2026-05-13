from math import ceil
from app.database import get_db

class PaginationHelper:
    @staticmethod
    def paginate_query(query, count_query, params, page=1, limit=20, sort_by="created_at", sort_order="desc"):
        db = get_db()
        page = max(1, page)
        limit = min(100, max(1, limit))
        offset = (page - 1) * limit
        allowed = ['id', 'created_at', 'updated_at', 'name', 'date', 'score', 'full_name']
        if sort_by not in allowed: sort_by = 'created_at'
        sort_order = 'ASC' if sort_order.lower() == 'asc' else 'DESC'
        total = db.fetch_one(count_query, params)
        total_count = total[0] if total else 0
        total_pages = ceil(total_count / limit) if total_count > 0 else 1
        paginated_query = f"{query} ORDER BY {sort_by} {sort_order} LIMIT ? OFFSET ?"
        rows = db.fetch_all(paginated_query, tuple(list(params) + [limit, offset]))
        return {"data": [dict(r) for r in rows] if rows else [], "pagination": {"page": page, "limit": limit, "total": total_count, "pages": total_pages, "has_next": page < total_pages, "has_prev": page > 1}}
