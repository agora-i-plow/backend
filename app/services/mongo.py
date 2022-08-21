from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.utils.exceptions import InternalServerError
from app.utils.get_settings import get_mongo_settings


class Mongo:
    client: AsyncIOMotorDatabase
    db: AsyncIOMotorDatabase

    @classmethod
    def connect_db(cls) -> None:
        settings = get_mongo_settings()
        try:
            cls.client = AsyncIOMotorClient(settings.db_uri)
            cls.db = cls.client[settings.MONGO_DATABASE]
        except Exception as e:
            raise InternalServerError(e) from e

    @classmethod
    def disconnect_db(cls) -> None:
        cls.client.close()
