from asyncio import gather
from dataclasses import dataclass

from asyncpg.exceptions import UniqueViolationError
from pymongo.errors import BulkWriteError

from app.models.base.base_user import Roles
from app.models.users.producer import Producer
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
class Admin(Producer):
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
        if user.role != Roles.ADMIN.value:
            raise ForbiddenException("User is not an admin")
        return user

    @staticmethod
    async def add(username: str, hashed_password: str):
        sql = """
            INSERT INTO users(username, hashed_password, role)
            VALUES ($1, $2, $3)
        """
        try:
            await Postgres.execute(sql, username, hashed_password, Roles.ADMIN.value)
        except UniqueViolationError as e:
            raise BadRequest("User already exists", e) from e

    @classmethod
    async def upload_references(cls, references: list[dict]) -> int:
        try:
            await Mongo.db["references"].insert_many(references, ordered=False)
        except BulkWriteError as e:
            return len(e.details["writeErrors"])
        return 0

    @classmethod
    async def relink_references(cls) -> int:
        async def exception_handler(func, item_id: str, reference_id: str) -> int:
            try:
                await func(item_id, reference_id)
                return 0
            except ItemNotFoundException as e:
                return 1

        coroutines = list()
        async for item in Mongo.db["items"].find():
            item_id = item["product_id"]
            reference_id = await match_item(format_item(item))
            coroutines.append(
                exception_handler(cls.manually_link, item_id, reference_id)
            )
        return sum(await gather(*coroutines))
