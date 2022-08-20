from datetime import timedelta

from fastapi import APIRouter, File, UploadFile
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.base.base_user import Roles
from app.models.users.producer import Producer
from app.models.users.admin import Admin
from app.utils.formatter import format_model
from app.utils.matching import match_item
from app.views.common import SuccessfullResponse, UserIn, FileIn
from app.views.admin import DuplicatesCounter
from app.views.producer import ItemIn
from app.utils.auth import get_password_hash,create_access_token, verify_password
from app.utils.exceptions import ForbiddenException, UserNotFoundException
from app.utils.file_parser import parse_json_file

preview_router = APIRouter(tags=["Превью метчера"])

# TODO: Написать где-то, что тут логика изолирована от бд в угоду скорости

@preview_router.post('/match_products')
async def upload_items_with_matching(items: list[dict]) -> list[dict[str,str]]:
    matched: list[dict[str,str]] = list()
    for item in items:
        reference_id = await match_item(item)
        matched.append({
            'id': item['id'], # Не product id
            'reference_id': reference_id
        })
    return matched