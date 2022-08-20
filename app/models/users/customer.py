from dataclasses import dataclass
from uuid import UUID
from asyncpg.exceptions import UniqueViolationError
from pymongo.errors import BulkWriteError
from app.services.postgres import Postgres
from app.services.mongo import Mongo
from app.models.base.base_user import BaseUser, Roles
from app.utils.exceptions import UserNotFoundException, ForbiddenException, BadRequest, ItemNotFoundException


class Customer:

    @classmethod
    async def get_references(cls) -> list[dict]:
        references = list()
        async for reference in Mongo.db['references'].find():
            references.append(reference)
        return references

    @classmethod
    async def get_items(cls) -> list[dict]:
        items = list()
        async for item in Mongo.db['items'].find():
            items.append(item)
        return items

    @classmethod
    async def references_search(cls, query: str) -> list[dict]:
        pass


    @classmethod
    async def items_search(cls, query: str) -> list[dict]:
        pass
