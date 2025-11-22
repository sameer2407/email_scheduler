from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from app.config import settings
import re

client = None
db = None


def is_atlas_connection(uri: str) -> bool:
    """Check if connection string is MongoDB Atlas (mongodb+srv://)."""
    return uri.startswith('mongodb+srv://')


def ensure_database_in_uri(uri: str, database_name: str) -> str:
    """Ensure database name is in the connection URI."""
    # Check if database name is already in URI
    if f'/{database_name}' in uri or f'/{database_name}?' in uri:
        return uri
    
    # Check if URI already has a database path
    if re.search(r'mongodb\+srv://[^/]+/[^/?]+', uri):
        # Replace existing database name
        uri = re.sub(r'(mongodb\+srv://[^/]+/)([^/?]+)', f'\\1{database_name}', uri)
    elif re.search(r'mongodb://[^/]+/[^/?]+', uri):
        # Replace existing database name for regular mongodb://
        uri = re.sub(r'(mongodb://[^/]+/)([^/?]+)', f'\\1{database_name}', uri)
    else:
        # Add database name before query parameters or at the end
        if '?' in uri:
            uri = uri.replace('?', f'/{database_name}?', 1)
        else:
            uri = f'{uri}/{database_name}'
    
    return uri


async def connect_db():
    """Connect to MongoDB (supports both Atlas and localhost)."""
    global client, db
    try:
        uri = settings.MONGODB_URL
        
        # Ensure database name is in the URI
        uri = ensure_database_in_uri(uri, settings.DATABASE_NAME)
        
        # Add ServerApi for Atlas connections (mongodb+srv://)
        if is_atlas_connection(uri):
            client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
            print(f"Connecting to MongoDB Atlas...")
        else:
            client = AsyncIOMotorClient(uri)
            print(f"Connecting to local MongoDB...")
        
        db = client[settings.DATABASE_NAME]
        
        # Test connection with ping
        await client.admin.command('ping')
        print(f"✓ Connected to MongoDB: {settings.DATABASE_NAME}")
        
        # Show connection type
        if is_atlas_connection(uri):
            print(f"  Connection type: MongoDB Atlas (Cloud)")
        else:
            print(f"  Connection type: Local MongoDB")
            
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise


async def close_db():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")


def get_database():
    return db
