from dataclasses import dataclass
from uuid import UUID
from asyncpg.exceptions import UniqueViolationError
from app.services.postgres import Postgres
from app.models.base.base_user import BaseUser, Roles
from app.utils.exceptions import UserNotFoundException, ForbiddenException, BadRequest

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
        if user.role is Roles.PRODUCER.value:
            raise ForbiddenException('User is not a producer')
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
            raise BadRequest('User already exists', e) from e

