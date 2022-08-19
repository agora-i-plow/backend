from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class BaseItem(ABC):

    @classmethod
    @abstractmethod
    async def get(cls, *args, **kwargs):
        pass
