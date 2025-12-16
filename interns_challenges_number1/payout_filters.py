from datetime import datetime
from typing import Optional, Dict, List


def build_payout_match(
    *,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    payment_start_date: Optional[datetime] = None,
    payment_end_date: Optional[datetime] = None,
    statuses: Optional[List[str]] = None,
    user_type: Optional[str] = None,
) -> Dict:
    """
    این تابع «مغز تصمیم‌گیری فیلترها» است.

    چرا جداست؟
    - چون API نباید فکر کند
    - چون دیتابیس نباید بداند ورودی از کجا آمده
    - چون فردا اگر FastAPI → Django شد
      این کد نباید حتی بلرزد

    این تابع:
    ✅ ورودی می‌گیرد
    ✅ تصمیم می‌گیرد
    ✅ یک dict ساده برمی‌گرداند

    ❌ کوئری اجرا نمی‌کند
    ❌ به Mongo یا Django کاری ندارد
    """

    match: Dict = {}

    # --------------------------------------------------
    # فیلتر تاریخ ساخت (created)
    # --------------------------------------------------
    if start_date or end_date:
        match["created"] = {}

        # اگر تاریخ شروع داریم، یعنی «از این تاریخ به بعد»
        if start_date:
            match["created"]["$gte"] = start_date

        # اگر تاریخ پایان داریم، یعنی «تا این تاریخ»
        if end_date:
            match["created"]["$lte"] = end_date

        # اگر هیچ شرطی نمانده، این کلید نباید وجود داشته باشد
        if not match["created"]:
            del match["created"]

    # --------------------------------------------------
    # فیلتر تاریخ پرداخت (payment_date)
    # --------------------------------------------------
    if payment_start_date or payment_end_date:
        match["payment_date"] = {}

        if payment_start_date:
            match["payment_date"]["$gte"] = payment_start_date

        if payment_end_date:
            match["payment_date"]["$lte"] = payment_end_date

        if not match["payment_date"]:
            del match["payment_date"]

    # --------------------------------------------------
    # نوع کاربر
    # --------------------------------------------------
    if user_type:
        # اگر داده‌ای داده نشد، ما حدس نمی‌زنیم
        match["user_type"] = user_type

    # --------------------------------------------------
    # وضعیت‌ها (paid, pending, ...)
    # --------------------------------------------------
    if statuses:
        # زبان دیتابیس با زبان API فرق دارد
        match["status"] = {"$in": statuses}

    return match
