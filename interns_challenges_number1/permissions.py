def ensure_admin(user_roles: list[str]):
    """
    این تابع یک «نگهبانِ خالص» است.

    چرا خالص؟
    - نه HTTP می‌شناسد
    - نه JWT
    - نه FastAPI
    - نه Django

    فقط یک سؤال دارد:
    ❓ آیا این user ادمین است یا نه؟
    """

    if not user_roles:
        raise PermissionError("User has no roles")

    if "admin" not in user_roles:
        raise PermissionError("Admin access required")

    # اگر اینجا رسیدیم یعنی عبور مجاز است
    return True
