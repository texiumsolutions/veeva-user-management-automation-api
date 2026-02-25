"""User model for MongoDB"""
from pymongo import ASCENDING
from core.database import get_db
from datetime import datetime


class User:
    """User model for MongoDB storage"""
    
    def __init__(self, email: str, first_name: str, last_name: str, user_name: str = None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name or email
        self.created_at = datetime.utcnow()
    
    @staticmethod
    def create_indexes():
        """Create indexes on users collection"""
        db = get_db()
        users_collection = db['users']
        users_collection.create_index([("email", ASCENDING)], unique=True)
        users_collection.create_index([("user_name", ASCENDING)], unique=True)
    
    @staticmethod
    def insert_user(user_data: dict):
        """Insert a new user into MongoDB"""
        db = get_db()
        users_collection = db['users']
        
        user_doc = {
            "email": user_data.get("email"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "user_name": user_data.get("user_name", user_data.get("email")),
            "created_at": datetime.utcnow()
        }
        
        result = users_collection.insert_one(user_doc)
        return result.inserted_id
    
    @staticmethod
    def find_user_by_email(email: str):
        """Find user by email"""
        db = get_db()
        users_collection = db['users']
        return users_collection.find_one({"email": email})
    
    @staticmethod
    def find_all_users():
        """Find all users"""
        db = get_db()
        users_collection = db['users']
        return list(users_collection.find({}, {"_id": 0}))
