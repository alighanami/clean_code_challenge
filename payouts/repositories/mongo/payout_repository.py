from typing import List, Dict
from payouts.repositories.mongo.client import get_mongo_client


def list_payouts(
    *,
    match: Dict,
    sorting: Dict,
    pagination: Dict,
) -> List[Dict]:

    client = get_mongo_client()
    db = client["clean_code_challenge"]
    collection = db["payouts"]

    cursor = collection.find(match)

    # -------------------------
    # Sorting
    # -------------------------
    if sorting:
        cursor = cursor.sort(
            sorting["field"],
            -1 if sorting["reverse"] else 1,
        )

    # -------------------------
    # Pagination
    # -------------------------
    cursor = cursor.skip(pagination["offset"]).limit(pagination["limit"])

    results = list(cursor)

    for item in results:
        item["id"] = str(item.pop("_id"))

    return results
