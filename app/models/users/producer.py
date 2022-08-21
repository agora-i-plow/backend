from dataclasses import dataclass
from uuid import UUID

from asyncpg.exceptions import UniqueViolationError
from pymongo.errors import BulkWriteError

from app.models.base.base_user import BaseUser, Roles
from app.services.mongo import Mongo
from app.services.postgres import Postgres
from app.utils.exceptions import (
    BadRequest,
    ForbiddenException,
    ItemNotFoundException,
    UserNotFoundException,
)
from app.utils.formatter import format_item
from app.utils.matching import match_item


@dataclass
class Producer(BaseUser):
    uuid: UUID
    username: str
    hashed_password: str
    role: Roles

    @classmethod
    async def get(cls, username: str):
        sql = """
            SELECT uuid, username, hashed_password, role
            FROM users
            WHERE username = $1
        """
        record = await Postgres.fetchrow(sql, username)
        if not record:
            raise UserNotFoundException
        user = cls._from_record(record)
        return user

    @staticmethod
    async def add(username: str, hashed_password: str):
        sql = """
            INSERT INTO users(username, hashed_password)
            VALUES ($1, $2)
        """
        try:
            await Postgres.execute(sql, username, hashed_password)
        except UniqueViolationError as e:
            raise BadRequest("User already exists", e) from e

    @classmethod
    async def upload_items(cls, items: list[dict]) -> int:
        try:
            await Mongo.db["items"].insert_many(items, ordered=False)
        except BulkWriteError as e:
            return len(e.details["writeErrors"])
        return 0

    @classmethod
    async def manually_link(cls, item_id: str, reference_id: str) -> None:
        item = await Mongo.db["items"].find_one({"product_id": item_id})
        if not item:
            raise ItemNotFoundException
        reference = await Mongo.db["references"].find_one({"product_id": reference_id})
        if not reference:
            raise ItemNotFoundException
        await Mongo.db["items"].update_one(
            {"product_id": item_id}, {"$set": {"reference_id": reference_id}}
        )

    @classmethod
    async def auto_link(cls, item_id: str) -> None:
        item = await Mongo.db["items"].find_one({"product_id": item_id})
        if not item:
            raise ItemNotFoundException
        reference_id = await match_item(format_item(item))
        await Mongo.db["items"].update_one(
            {"product_id": item_id}, {"$set": {"reference_id": reference_id}}
        )
