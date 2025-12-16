def paginate(page: int | None, page_size: int):
    """
    ✅ Pagination خالص
    - نه Mongo می‌شناسد
    - نه FastAPI
    - فقط ریاضی
    """

    if page is None:
        return {
            "mode": "all"
        }

    if page < 1:
        page = 1

    offset = (page - 1) * page_size

    return {
        "mode": "page",
        "page": page,
        "offset": offset,
        "limit": page_size,
    }
