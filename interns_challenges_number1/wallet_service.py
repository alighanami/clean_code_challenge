async def check_available_balance(user_id):
    user_id = await check_is_valid_objectId(user_id)

    wallet = wallet_collection.find_one({"user_id": user_id})

    available_balance = wallet["available_balance"]
    pending_balance = 0
    transactions_to_delete = []

    for transaction in wallet["transactions"]:
        if transaction["date_available"] <= datetime.datetime.now():
            available_balance += transaction["amount"]
            transactions_to_delete.append(transaction["id"])
        else:
            pending_balance += transaction["amount"]

    wallet_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "available_balance": available_balance,
                "pending_balance": pending_balance,
            },
            "$pull": {
                "transactions": {"id": {"$in": transactions_to_delete}}
            },
        },
    )

    return available_balance, pending_balance