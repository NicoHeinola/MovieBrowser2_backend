from typing import Any, Dict
from sqlalchemy.orm import Query


def paginate_query(query: Query, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    page = int(page)
    page_size = int(page_size)

    if page < 1:
        page = 1
    total = query.count()
    pages = (total + page_size - 1) // page_size
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"pagination": {"total": total, "page": page, "pages": pages, "limit": page_size}, "data": items}
