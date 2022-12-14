from dataclasses import asdict
from traceback import format_exception
from typing import Type, TypeVar

from pydantic import BaseModel

from app.models.base.base_user import BaseUser

T = TypeVar("T", bound=Type[BaseModel])


def format_models(raw_models: list[BaseUser], model: T) -> list[T]:
    if not raw_models:
        return []
    return list(map(lambda x: model(**asdict(x)), raw_models))


def format_model(raw_models: BaseUser, model: T) -> T | None:
    if not raw_models:
        return None
    return model(**asdict(raw_models))


def format_items(items: list[dict]) -> list[dict]:
    return [
        {
            k: v
            for k, v in item.items()
            if k
            not in {
                "_id",
            }
        }
        for item in items
    ]


def format_item(item: dict) -> dict:
    return {
        k: v
        for k, v in item.items()
        if k
        not in {
            "_id",
        }
    }


def trim_extra_whitespaces(text: str) -> str:
    return " ".join(text.split())


def format_error(error: Exception) -> str:
    if not error:
        return ""
    lines = format_exception(type(error), error, error.__traceback__)
    return "\n".join(lines)
