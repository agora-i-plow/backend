from datetime import timedelta

from fastapi import APIRouter, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.base.base_user import Roles
from app.models.users.producer import Producer
from app.models.users.admin import Admin
from app.utils.formatter import format_model
from app.views.common import SuccessfullResponse, UserIn, FileIn
from app.views.admin import DuplicatesCounter
from app.utils.auth import get_password_hash,create_access_token, verify_password
from app.utils.exceptions import ForbiddenException, UserNotFoundException
from app.utils.file_parser import parse_json_file

admin_router = APIRouter(tags=["Функции админа"])

@admin_router.post('/admin/upload')
async def upload_reference(references: list[dict], user_in: UserIn = Depends()) -> DuplicatesCounter:
    admin = await Admin.get(user_in.username)
    duplicates = await admin.upload_references(references)
    return DuplicatesCounter(duplicates=duplicates)

@admin_router.post('/admin/upload/file')
async def upload_reference(file_in: FileIn = Depends(), user_in: UserIn = Depends()) -> DuplicatesCounter:
    admin = await Admin.get(user_in.username)
    references = parse_json_file(file_in.file)
    duplicates = await admin.upload_references(references)
    return DuplicatesCounter(duplicates=duplicates)


@admin_router.post('/admin/relink')
async def relink_items(user_in: UserIn = Depends()) -> SuccessfullResponse:
    admin = await Admin.get(user_in.username)
    await admin.relink_references()
    return SuccessfullResponse()