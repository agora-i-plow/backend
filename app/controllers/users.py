from datetime import timedelta

from fastapi import APIRouter, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.base.base_user import Roles
from app.models.users.producer import Producer
from app.models.users.admin import Admin
from app.utils.formatter import format_model
from app.views.common import UserOut, UserIn, TokenOut, SuccessfullResponse
from app.utils.auth import get_password_hash,create_access_token, verify_password
from app.utils.exceptions import ForbiddenException, UserNotFoundException

users_router = APIRouter(tags=["Функции пользователей"])

async def get_user_class(username: str) -> Producer | Admin:
    for classname in [Producer, Admin]:
        try:
            user = await classname.get(username)
            return user
        except ForbiddenException:
            continue
        except UserNotFoundException:
            continue
    raise UserNotFoundException

@users_router.post('/user/register', response_model=SuccessfullResponse)
async def user_register(
        role: Roles = Form(..., description='Роль аккаунта'),
        request: OAuth2PasswordRequestForm = Depends()) -> SuccessfullResponse:
    request.password = get_password_hash(request.password)
    if role == Roles.PRODUCER:
        await Producer.add(request.username, request.password)
    elif role == Roles.ADMIN:
        await Admin.add(request.username, request.password)
    return SuccessfullResponse()

@users_router.post('/user/login', response_model=TokenOut)
async def user_login(request: OAuth2PasswordRequestForm = Depends()) -> TokenOut:
    user = await get_user_class(request.username)
    if not verify_password(request.password, user.hashed_password):
        raise ForbiddenException('Wrong password')
    access_token = create_access_token(
        data={"sub": user.username}
    )
    token = TokenOut(access_token=access_token, token_type='bearer')
    return token

@users_router.get('/user', response_model=UserOut)
async def get_user(user_in: UserIn = Depends()) -> UserOut | None:
    user = await get_user_class(user_in.username)
    return format_model(user, UserOut)

