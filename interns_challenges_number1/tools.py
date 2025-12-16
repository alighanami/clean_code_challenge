# ============================================
# تنظیم پیش‌فرض تعداد آیتم در هر صفحه
# این مقدار فقط برای API معنی دارد
# منطق Pagination خودش از این عدد خبر ندارد
# ============================================

import datetime
from typing import List

from fastapi import HTTPException
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from wallet_service import check_available_balance

from d_2 import wallet_collection
from pagination import paginate  # ✅ منطق خالص Pagination
DEFAULT_PAGE_SIZE = 3


# ============================================
# بررسی معتبر بودن ObjectId
# --------------------------------------------
# ❗️این تابع Adapter است
# منطق بیزنسی نیست
# فقط خطای دیتابیس را به خطای HTTP ترجمه می‌کند
# ============================================
async def check_is_valid_objectId(id):
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(detail="not valid object id", status_code=400)


# ============================================
# ساخت Response نهایی Pagination برای API
# --------------------------------------------
# ✅ اینجا منطق Pagination نداریم
# ✅ فقط نتیجه آماده‌شده را در قالب Response می‌ریزیم
# ============================================
async def create_paginate_response(page, collection, match, add_wallet=False):
    page, total_docs, result = await paginate_results(
        page, collection, match, add_wallet
    )

    # محاسبه تعداد کل صفحات
    # این محاسبه هنوز API-level است
    total_pages = (
        -(-total_docs // DEFAULT_PAGE_SIZE)
        if page is not None
        else 1
    )

    return {
        "page": page,
        "pageSize": DEFAULT_PAGE_SIZE,
        "totalPages": total_pages,
        "totalDocs": total_docs,
        "results": result,
    }


# ============================================
# Adapter اصلی Pagination با MongoDB
# --------------------------------------------
# ❗️اینجا مهم‌ترین مرز معماری است
# - Pagination خالص فقط عدد می‌دهد
# - Mongo فقط مصرف‌کننده آن اعداد است
# ============================================
async def paginate_results(page, collection, match, add_wallet=False):
    # گرفتن خروجی خالص Pagination
    pagination = paginate(page, DEFAULT_PAGE_SIZE)

    # ----------------------------------------
    # حالت اول: صفحه مشخص نشده → همه داده‌ها
    # ----------------------------------------
    if pagination["mode"] == "all":
        cursor = collection.find(match)
        result = list(cursor)

        for index, doc in enumerate(result):
            # تبدیل ObjectId به string برای API
            doc["_id"] = str(doc["_id"])

            if "affiliate_tracking_id" in doc:
                doc["affiliate_tracking_id"] = str(doc["affiliate_tracking_id"])

            if "user_id" in doc:
                doc["user_id"] = str(doc["user_id"])

            # اگر Wallet لازم باشد، منطق بیزنسی جداگانه صدا زده می‌شود
            if add_wallet:
                available_balance, pending_balance = await check_available_balance(
                    doc["_id"]
                )
                doc["available_balance"] = available_balance
                doc["pending_balance"] = pending_balance

            # تبدیل snake_case به camelCase برای API
            result[index] = await convert_dict_camel_case(doc)

        # page در این حالت معنی ندارد
        return None, len(result), result

    # ----------------------------------------
    # حالت دوم: Pagination فعال
    # ----------------------------------------
    total_docs = collection.count_documents(match)

    # مصرف offset / limit محاسبه‌شده توسط منطق خالص
    cursor = (
        collection
        .find(match)
        .skip(pagination["offset"])
        .limit(pagination["limit"])
    )

    result = await paginate_documents(
        cursor,
        pagination["offset"],
        pagination["limit"],
        add_wallet
    )

    return pagination["page"], total_docs, result


# ============================================
# منطق بیزنسی Wallet
# --------------------------------------------
# ❗️این تابع Business Logic است
# بعداً در Stage 6.5 باید از این فایل خارج شود
# ============================================



# ============================================
# Helper: snake_case → camelCase
# --------------------------------------------
# Helper است، نه بیزنس، نه Adapter
# ============================================
async def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


async def convert_dict_camel_case(data):
    camel_dict = {}
    for key, value in data.items():
        camel_key = await snake_to_camel(key)
        camel_dict[camel_key] = value
    return camel_dict


# ============================================
# Pagination روی Cursor Mongo
# --------------------------------------------
# ❗️اینجا Mongo-specific است
# ولی Pagination Logic ندارد
# ============================================
async def paginate_documents(
    cursor: Cursor,
    skip: int,
    limit: int,
    add_wallet=False
) -> List[dict]:

    result = [doc for doc in cursor]

    for index, doc in enumerate(result):
        original_id = doc["_id"]
        doc["_id"] = str(doc["_id"])

        if "affiliate_tracking_id" in doc:
            doc["affiliate_tracking_id"] = str(doc["affiliate_tracking_id"])

        if "user_id" in doc:
            doc["user_id"] = str(doc["user_id"])

        # تبدیل کلیدها برای API
        doc = await convert_dict_camel_case(doc)

        if add_wallet:
            available_balance, pending_balance = await check_available_balance(
                original_id
            )
            doc["availableBalance"] = available_balance
            doc["pendingBalance"] = pending_balance

        result[index] = doc

    return result
