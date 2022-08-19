from dataclasses import dataclass
from uuid import UUID
from asyncpg.exceptions import UniqueViolationError
from app.services.postgres import Postgres
from app.models.base.base_user import BaseUser, Roles
from app.utils.exceptions import UserNotFoundException, ForbiddenException, BadRequest

@dataclass
class Admin(BaseUser):
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


