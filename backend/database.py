from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection with error handling
mongo_url = os.environ.get('MONGO_URL')
if not mongo_url:
    raise ValueError("MONGO_URL environment variable is required. Please set it in your deployment environment.")

<<<<<<< HEAD
try:
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'farmchat')]
    print(f"✅ MongoDB connection configured for: {mongo_url.split('@')[1] if '@' in mongo_url else 'localhost'}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    raise

async def get_database():
    """Get database instance"""
=======
# Try to connect to MongoDB, but don't fail if it's not available
client = None
db = None
mongodb_available = False

try:
    # Try to connect with a very short timeout
    import asyncio
    from pymongo import MongoClient
    
    # Use synchronous client for connection test
    test_client = MongoClient(mongo_url, serverSelectionTimeoutMS=1000)
    test_client.admin.command('ping')
    test_client.close()
    
    # If we get here, MongoDB is available
    client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
    db = client[os.environ.get('DB_NAME', 'farmchat')]
    mongodb_available = True
    print(f"✅ MongoDB connection successful: {mongo_url.split('@')[1] if '@' in mongo_url else 'localhost'}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("💡 Using mock database for development")
    print("   To use real MongoDB: brew install mongodb-community && brew services start mongodb-community")
    client = None
    db = None
    mongodb_available = False

class MockCollection:
    """Mock MongoDB collection for development without database"""
    async def insert_one(self, document):
        print(f"Mock DB: Inserting document into collection")
        return type('MockResult', (), {'inserted_id': 'mock_id_123'})()
    
    async def insert_many(self, documents):
        print(f"Mock DB: Inserting {len(documents)} documents into collection")
        return type('MockResult', (), {'inserted_ids': ['mock_id_1', 'mock_id_2']})()
    
    async def find_one(self, query):
        print(f"Mock DB: Finding one document with query: {query}")
        return None  # Always return None (user not found)
    
    async def update_one(self, query, update, **kwargs):
        print(f"Mock DB: Updating document with query: {query}")
        return type('MockResult', (), {'modified_count': 1})()
    
    async def delete_one(self, query):
        print(f"Mock DB: Deleting document with query: {query}")
        return type('MockResult', (), {'deleted_count': 1})()
    
    async def delete_many(self, query):
        print(f"Mock DB: Deleting many documents with query: {query}")
        return type('MockResult', (), {'deleted_count': 0})()
    
    def find(self, query=None, projection=None):
        print(f"Mock DB: Finding documents with query: {query}")
        return MockCursor()

class MockCursor:
    """Mock MongoDB cursor with full method support"""
    def __init__(self):
        self._data = []
    
    async def to_list(self, length):
        return []
    
    def sort(self, field, direction=1):
        print(f"Mock DB: Sorting by {field}")
        return self
    
    def limit(self, count):
        print(f"Mock DB: Limiting to {count} documents")
        return self
    
    def skip(self, count):
        print(f"Mock DB: Skipping {count} documents")
        return self

class MockDatabase:
    """Mock MongoDB database for development"""
    def __getattr__(self, name):
        print(f"Mock DB: Accessing collection '{name}'")
        return MockCollection()
    
    async def command(self, command_name):
        """Mock database command for health checks"""
        print(f"Mock DB: Executing command '{command_name}'")
        return {"ok": 1}

async def get_database():
    """Get database instance"""
    if not mongodb_available or db is None:
        print("Using mock database for development")
        return MockDatabase()
>>>>>>> c7ba531 (Initial push: migrate local codebase to KisanMitr)
    return db

async def close_database():
    """Close database connection"""
    client.close()