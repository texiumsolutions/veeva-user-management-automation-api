"""Connection model for MongoDB - External system integrations"""

from pymongo import ASCENDING
from core.database import get_db
from datetime import datetime
from bson import ObjectId


class Connection:
    """Connection model for storing system integrations"""

    COLLECTION = "integration"

    @staticmethod
    def create_indexes():
        db = get_db()
        collection = db[Connection.COLLECTION]

        collection.create_index([("connectionName", ASCENDING)], unique=True)
        collection.create_index([("type", ASCENDING)])
        collection.create_index([("environment", ASCENDING)])

    @staticmethod
    def insert_connection(connection_data: dict):

        db = get_db()
        collection = db[Connection.COLLECTION]

        connection_doc = {
            "connectionName": connection_data.get("connectionName"),
            "description": connection_data.get("description", ""),
            "type": connection_data.get("type"),
            "environment": connection_data.get("environment", "production"),

            # integration-specific configuration
            "config": connection_data.get("config", {}),

            # authentication details
            "credentials": connection_data.get("credentials", {}),

            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = collection.insert_one(connection_doc)
        return str(result.inserted_id)

    @staticmethod
    def find_connection_by_id(connection_id: str):

        db = get_db()
        collection = db[Connection.COLLECTION]

        try:
            return collection.find_one({"_id": ObjectId(connection_id)})
        except Exception:
            return None

    @staticmethod
    def find_connection_by_name(connection_name: str):

        db = get_db()
        collection = db[Connection.COLLECTION]

        return collection.find_one({"connectionName": connection_name})

    @staticmethod
    def find_all_connections():

        db = get_db()
        collection = db[Connection.COLLECTION]

        return list(collection.find())

    @staticmethod
    def update_connection(connection_id: str, connection_data: dict):

        db = get_db()
        collection = db[Connection.COLLECTION]

        update_data = {k: v for k, v in connection_data.items() if k != "_id"}
        update_data["updated_at"] = datetime.utcnow()

        try:
            result = collection.update_one(
                {"_id": ObjectId(connection_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception:
            return False

    @staticmethod
    def delete_connection(connection_id: str):

        db = get_db()
        collection = db[Connection.COLLECTION]

        try:
            result = collection.delete_one({"_id": ObjectId(connection_id)})
            return result.deleted_count > 0
        except Exception:
            return False