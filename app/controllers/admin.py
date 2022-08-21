from fastapi import APIRouter
from fastapi.param_functions import Depends

from app.models.users.admin import Admin
from app.utils.file_parser import parse_json_file
from app.views.admin import DuplicatesCounter, ErrorsCounter
from app.views.common import FileIn, UserIn

admin_router = APIRouter(tags=["Функции админа"])


@admin_router.post("/admin/upload")
async def upload_reference(
    references: list[dict], user_in: UserIn = Depends()
) -> DuplicatesCounter:
    admin = await Admin.get(user_in.username)
    duplicates = await admin.upload_references(references)
    return DuplicatesCounter(duplicates=duplicates)


@admin_router.post("/admin/upload/file")
async def upload_reference(
    file_in: FileIn = Depends(), user_in: UserIn = Depends()
) -> DuplicatesCounter:
    admin = await Admin.get(user_in.username)
    references = parse_json_file(file_in.file)
    duplicates = await admin.upload_references(references)
    return DuplicatesCounter(duplicates=duplicates)


@admin_router.post("/admin/relink")
async def relink_items(user_in: UserIn = Depends()) -> ErrorsCounter:
    admin = await Admin.get(user_in.username)
    errors = await admin.relink_references()
    return ErrorsCounter(errors=errors)
