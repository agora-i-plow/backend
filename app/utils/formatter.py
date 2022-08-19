from dataclasses import asdict
from typing import TypeVar, Type
from traceback import format_exception
from pydantic import BaseModel
from app.models.base.base_item import BaseItem
from app.models.base.base_user import BaseUser

T = TypeVar('T',bound=Type[BaseModel])

def format_models(raw_models: list[BaseItem | BaseUser], model: T) -> list[T]:
    if not raw_models:
        return []
    return list(map(lambda x: model(**asdict(x)), raw_models))

def format_model(raw_models: BaseItem | BaseUser, model: T) -> T | None:
    if not raw_models:
        return None
    return model(**asdict(raw_models))

def trim_extra_whitespaces(text: str) -> str:
    return ' '.join(text.split())

def format_error(error: Exception) -> str:
    if not error:
        return ''
    lines = format_exception(type(error), error, error.__traceback__)
    return '\n'.join(lines)
