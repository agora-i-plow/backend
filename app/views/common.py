from fastapi import Depends, UploadFile, File
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.base.base_user import Roles
from app.utils.auth import get_current_user

class SuccessfullResponse(BaseModel):
    details: str = Field('Выполнено', title='Статус операции')

class TokenOut(BaseModel):
    access_token: str = Field(..., description='Access token')
    token_type: str = Field(..., description='Token type')

class UserOut(BaseModel):
    uuid: UUID = Field(None, description='UUID пользователя')
    username: str = Field(None, description='Имя аккаунта')
    role: Roles = Field(None, description='Роль аккаунта')

class UserIn(BaseModel):
    username: str = Depends(get_current_user)

class FileIn(BaseModel):
    file: UploadFile = File(..., description='File in json format')
