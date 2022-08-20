import asyncio
from datetime import timedelta
from fastapi import APIRouter, File, UploadFile, Body
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.base.base_user import Roles
from app.models.users.producer import Producer
from app.models.users.admin import Admin
from app.utils.formatter import format_model
from app.utils.matching import match_item
from app.views.customer import MatchedOut
from app.views.common import SuccessfullResponse, UserIn, FileIn
from app.views.admin import DuplicatesCounter
from app.views.producer import ItemIn
from app.utils.logger import Log
from app.utils.auth import get_password_hash,create_access_token, verify_password
from app.utils.exceptions import ForbiddenException, UserNotFoundException
from app.utils.file_parser import parse_json_file

preview_router = APIRouter(tags=["Превью метчера"])

# TODO: Написать где-то, что тут логика изолирована от бд в угоду скорости

@preview_router.post('/match_products', responses={
    200: {
        'description': 'List of dicts containing item id and matched reference id',
        'content': {
            'application/json': {
                'example': [
                    {
                        'id': '0039af5efceac4ab',
                        'reference_id': '28085e941cde1639'
                    },
                    {
                        'id': '004f2158acb8165c',
                        'reference_id': '9afe55bb4bf1e8a8'
                    }
                ]
            }
        }
    }
})
async def upload_items_with_matching(items: list[dict] = Body(..., example=[
    {
        "id": "0039af5efceac4ab",
        "name": "Холодильник Бирюса 118",
        "props": [
            "Мощность  замораживания  4 кг/сутки"
        ]
    },
    {
        "id": "004f2158acb8165c",
        "name": "ASUS TUF-GTX1660S-O6G-GAMING Видеокарта",
        "props": [
            "Объем  видеопамяти\t6144 МБ",
            "Частота  памяти\t14002 МГц",
            "Разъемы   и интерфейсы выход DVI, выход DisplayPort, выход HDMI"
        ]
    },
])) -> list[dict[str,str]]:
    async def converter(item):
        reference_id = await match_item(item)
        return {
            'id': item['product_id'],
            'reference_id': reference_id
        }
    matched: list[dict[str,str]] = list()
    coroutines = list()
    for item in items:
        coroutines.append(converter(item))
    matched = await asyncio.gather(*coroutines)
    return matched