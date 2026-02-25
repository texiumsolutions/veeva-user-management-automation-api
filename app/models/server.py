"""Server model for MongoDB"""
from pymongo import ASCENDING
from core.database import get_db
from datetime import datetime
from bson import ObjectId


class Server:
    """Server model for MongoDB storage"""
    
    def __init__(self, user_id: str, name: str, hostname: str, port: int, connection_name: str, instance_url: str, username: str, password: str, status: str = "running"):
        self.user_id = user_id
        self.name = name
        self.hostname = hostname
        self.port = port
        self.connection_name = connection_name
        self.instance_url = instance_url
        self.username = username
        self.password = password
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    @staticmethod
    def create_indexes():
        """Create indexes on servers collection"""
        db = get_db()
        servers_collection = db['servers']
        servers_collection.create_index([("user_id", ASCENDING)])
        servers_collection.create_index([("name", ASCENDING)])
        servers_collection.create_index([("hostname", ASCENDING)])
    
    @staticmethod
    def insert_server(server_data: dict):
        """Insert a new server into MongoDB"""
        db = get_db()
        servers_collection = db['servers']
        
        server_doc = {
            "user_id": ObjectId(server_data.get("user_id")) if isinstance(server_data.get("user_id"), str) else server_data.get("user_id"),
            "name": server_data.get("name"),
            "hostname": server_data.get("hostname"),
            "port": server_data.get("port"),
            "status": server_data.get("status", "running"),
            "connection_name": server_data.get("connection_name"),
            "instance_url": server_data.get("instance_url"),
            "username": server_data.get("username"),
            "password": server_data.get("password"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = servers_collection.insert_one(server_doc)
        return result.inserted_id
    
    @staticmethod
    def find_server_by_id(server_id: str):
        """Find server by ID"""
        db = get_db()
        servers_collection = db['servers']
        try:
            return servers_collection.find_one({"_id": ObjectId(server_id)})
        except:
            return None
    
    @staticmethod
    def find_servers_by_user(user_id: str):
        """Find all servers for a user"""
        db = get_db()
        servers_collection = db['servers']
        try:
            return list(servers_collection.find({"user_id": ObjectId(user_id)}))
        except:
            return []
    
    @staticmethod
    def find_all_servers():
        """Find all servers"""
        db = get_db()
        servers_collection = db['servers']
        return list(servers_collection.find({}))
    
    @staticmethod
    def update_server(server_id: str, update_data: dict):
        """Update a server"""
        db = get_db()
        servers_collection = db['servers']
        
        try:
            # Remove fields that shouldn't be updated
            update_data.pop("_id", None)
            update_data.pop("user_id", None)
            update_data.pop("created_at", None)
            
            update_data["updated_at"] = datetime.utcnow()
            
            result = servers_collection.update_one(
                {"_id": ObjectId(server_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    @staticmethod
    def delete_server(server_id: str):
        """Delete a server"""
        db = get_db()
        servers_collection = db['servers']
        
        try:
            result = servers_collection.delete_one({"_id": ObjectId(server_id)})
            return result.deleted_count > 0
        except:
            return False
    
    @staticmethod
    def delete_servers_by_user(user_id: str):
        """Delete all servers for a user"""
        db = get_db()
        servers_collection = db['servers']
        
        try:
            result = servers_collection.delete_many({"user_id": ObjectId(user_id)})
            return result.deleted_count
        except:
            return 0
