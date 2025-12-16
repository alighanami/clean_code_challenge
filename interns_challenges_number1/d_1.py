from fastapi import HTTPException, Header
import jwt
import os

from d_2 import user_collection
from permissions import ensure_admin


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
expiration_time = os.getenv("JWT_EXPIRATION_MINUTES") or 0
JWT_EXPIRATION_MINUTES = int(expiration_time)


async def check_user_is_admin(authorization: str = Header(...)):
    """
    این تابع «نگهبان» نیست.
    این تابع فقط مترجم دنیای HTTP → دنیای Logic است.

    وظیفه‌ها:
    - توکن را از Header بخواند
    - کاربر را پیدا کند
    - roleها را استخراج کند
    - تصمیم‌گیری را بسپارد به ensure_admin
    """

    email = await get_email_from_token(authorization)

    user = user_collection.find_one({'email': email})
    if user is None:
        raise HTTPException(detail='User not found', status_code=404)

    # -------------------------------
    # ✅ استخراج roleها
    # API فقط «داده» می‌دهد
    # Logic تصمیم می‌گیرد
    # -------------------------------
    user_roles = [user.get("user_type")]

    try:
        ensure_admin(user_roles)
    except PermissionError as e:
        raise HTTPException(detail=str(e), status_code=403)

    # FastAPI به Depends نیاز دارد چیزی برگردد
    return user


async def get_email_from_token(authorization: str = Header(...)):
    """
    این تابع فقط کار Token را می‌کند.
    نه Permission
    نه Business Rule
    """

    try:
        decode_token = decode_jwt_token(authorization)
        email = decode_token["sub"]
    except Exception as e:
        raise HTTPException(detail="Invalid token", status_code=400)

    return email


def decode_jwt_token(token: str):
    """
    فقط Decode.
    هیچ تصمیمی اینجا نباید گرفته شود.
    """

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(detail="Invalid token", status_code=400)


async def get_status_list_from_query(statuses):
    """
    Utility function
    (این به مرحله ۵ ربطی ندارد، فعلاً دست نمی‌زنیم)
    """

    status_list = statuses.split(",")
    return [status.strip() for status in status_list]
