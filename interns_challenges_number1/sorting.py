# ============================================
# منطق خالص Sorting / Ordering
# --------------------------------------------
# ❗️هیچ Mongo / Django / ORM اینجا نباید باشد
# ============================================

def build_sorting(sort_by: str | None, direction: str | None):
    # اگر کاربر Sorting نخواست
    if not sort_by:
        return None

    direction = (direction or "asc").lower()

    if direction not in ("asc", "desc"):
        raise ValueError("Invalid sort direction")

    return {
        "field": sort_by,
        "reverse": direction == "desc",
    }
