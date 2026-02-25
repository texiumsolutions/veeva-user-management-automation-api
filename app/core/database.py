"""Database connection module"""
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "texium_db")

# MongoDB client
client = None
db = None

print("MONGO URI:", MONGO_URI)
print("DB NAME:", DB_NAME)

def connect_to_mongo():
    """Establish connection to MongoDB"""
    global client, db
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        db = client[DB_NAME]
        print(f"✓ Connected to MongoDB: {DB_NAME}")
        return db
    except ServerSelectionTimeoutError:
        print("✗ Failed to connect to MongoDB. Make sure MongoDB is running.")
        raise


def get_db():
    """Get database instance"""
    global db
    if db is None:
        connect_to_mongo()
    return db


def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("✓ MongoDB connection closed")
