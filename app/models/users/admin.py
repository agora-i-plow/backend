from asyncio import gather
from dataclasses import dataclass
from uuid import UUID
from asyncpg.exceptions import UniqueViolationError
from pymongo.errors import BulkWriteError
from app.services.postgres import Postgres
from app.services.mongo import Mongo
from app.models.users.producer import Producer
from app.models.base.base_user import Roles
from app.utils.exceptions import UserNotFoundException, ForbiddenException, BadRequest

# TODO: Сделать счетчик ошибок в релинке

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
            raise ForbiddenException('User is not an admin')
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
            raise BadRequest('User already exists', e) from e

    @classmethod
    async def upload_references(cls, references: list[dict]) -> int:
        try:
            await Mongo.db['references'].insert_many(references, ordered=False)
        except BulkWriteError as e:
            return len(e.details['writeErrors'])
        return 0

    @classmethod
    async def relink_references(cls) -> None:
        coroutines = list()
        async for item in Mongo.db['references'].find():
            item_id = item['product_id']
            reference_id = None # <------------------------- ML here
            coroutines.append(cls.manually_link(item_id, reference_id))
        await gather(coroutines)