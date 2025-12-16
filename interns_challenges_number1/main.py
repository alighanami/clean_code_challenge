from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Depends

from d_1 import check_user_is_admin, get_status_list_from_query
from d_2 import payout_collection
from tools import create_paginate_response
from payout_filters import build_payout_match
from sorting import build_sorting  # ✅ Stage 7: منطق خالص Sorting


router = FastAPI()


@router.get("/payout")
async def all_payout(
    # --------------------------------------------
    # Query Params مربوط به Filter
    # --------------------------------------------
    statuses: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    payment_start_date: Optional[datetime] = None,
    payment_end_date: Optional[datetime] = None,
    user_type: Optional[str] = None,

    # --------------------------------------------
    # Pagination
    # --------------------------------------------
    page: Optional[int] = None,

    # --------------------------------------------
    # ✅ Stage 7: Sorting (فقط ورودی)
    # --------------------------------------------
    sort_by: Optional[str] = None,
    direction: Optional[str] = "desc",

    # --------------------------------------------
    # Permission
    # --------------------------------------------
    admin: str = Depends(check_user_is_admin),
):
    # --------------------------------------------
    # API فقط ورودی‌ها را جمع می‌کند
    # هیچ تصمیم بیزنسی اینجا گرفته نمی‌شود
    # --------------------------------------------

    status_list = None
    if statuses:
        status_list = await get_status_list_from_query(statuses)

    # --------------------------------------------
    # Filter Logic (Pure)
    # --------------------------------------------
    match = build_payout_match(
        start_date=start_date,
        end_date=end_date,
        payment_start_date=payment_start_date,
        payment_end_date=payment_end_date,
        user_type=user_type,
        statuses=status_list,
    )

    # --------------------------------------------
    # ✅ Stage 7: Sorting Logic (Pure)
    # --------------------------------------------
    sorting = build_sorting(sort_by, direction)

    # ❗️در این مرحله sorting فقط «محاسبه» می‌شود
    # ❗️مصرف آن در Adapter / DB لایه بعدی است
    # ❗️Extraction ≠ Implementation

    return await create_paginate_response(
        page=page,
        collection=payout_collection,
        match=match,
        # sorting فعلاً به Mongo وصل نشده (طبق Stage 7)
    )
