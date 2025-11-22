from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None
db = None


async def connect_db():
    global client, db
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        await client.admin.command('ping')
        print(f"Connected to MongoDB: {settings.DATABASE_NAME}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


async def close_db():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")


def get_database():
    return db
