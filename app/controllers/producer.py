from datetime import timedelta

from fastapi import APIRouter, File, UploadFile
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.base.base_user import Roles
from app.models.users.producer import Producer
from app.models.users.admin import Admin
from app.utils.formatter import format_model
from app.views.common import SuccessfullResponse, UserIn, FileIn
from app.views.admin import DuplicatesCounter
from app.views.producer import ItemIn
from app.utils.auth import get_password_hash,create_access_token, verify_password
from app.utils.exceptions import ForbiddenException, UserNotFoundException
from app.utils.file_parser import parse_json_file

producer_router = APIRouter(tags=["Функции производителя"])

@producer_router.post('/producer/upload')
async def upload_item(items: list[dict], user_in: UserIn = Depends()) -> DuplicatesCounter:
    producer = await Producer.get(user_in.username)
    duplicates = await producer.upload_items(items)
    return DuplicatesCounter(duplicates=duplicates)

@producer_router.post('/producer/upload/file')
async def upload_item_using_file(file_in: FileIn = Depends(), user_in: UserIn = Depends()) -> DuplicatesCounter:
    producer = await Producer.get(user_in.username)
    items = parse_json_file(file_in.file)
    duplicates = await producer.upload_items(items)
    return DuplicatesCounter(duplicates=duplicates)

@producer_router.post('/producer/link/manual')
async def manually_link_item(item_in: ItemIn, reference_in: ItemIn, user_in: UserIn = Depends()) -> SuccessfullResponse:
    producer = await Producer.get(user_in.username)
    await producer.manually_link(item_in.product_id, reference_in.product_id)
    return SuccessfullResponse()

@producer_router.post('/producer/link/auto')
async def auto_link_item(item_in: ItemIn, user_in: UserIn = Depends()) -> SuccessfullResponse:
    producer = await Producer.get(user_in.username)
    await producer.auto_link(item_in.product_id)
    return SuccessfullResponse()