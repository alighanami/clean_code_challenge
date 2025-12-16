from pymongo import MongoClient
from django.conf import settings

_client = None


def get_mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
    return _client


def get_payouts_collection():
    client = get_mongo_client()
    db = client[settings.MONGO_DB_NAME]
    return db[settings.MONGO_PAYOUTS_COLLECTION]