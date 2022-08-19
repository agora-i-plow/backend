from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod
from asyncpg import Record

class Roles(Enum):
    PRODUCER: str = 'producer'
    ADMIN: str = 'admin'

@dataclass
class BaseUser(ABC):

    @classmethod
    def _from_record(cls, record: Record, **kwargs):
        return cls(**record, **kwargs)

    @classmethod
    def _from_records(cls, records: list[Record], **kwargs):
        return [cls._from_record(record, **kwargs) for record in records]

    @classmethod
    @abstractmethod
    async def get(cls, *args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    async def add(username: str, hashed_password: str):
        pass
