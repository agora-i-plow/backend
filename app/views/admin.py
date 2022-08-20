from fastapi import Depends
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.base.base_user import Roles
from app.utils.auth import get_current_user

class DuplicatesCounter(BaseModel):
    duplicates: int = Field(0, description='Number of duplicates')

class ErrorsCounter(BaseModel):
    errors: int = Field(0, description='Number of errors')