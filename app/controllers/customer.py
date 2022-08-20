from datetime import timedelta

from fastapi import APIRouter, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.base.base_user import Roles
from app.models.users.producer import Producer
from app.models.users.admin import Admin
from app.utils.formatter import format_items
from app.views.common import SuccessfullResponse, UserIn
from app.views.admin import DuplicatesCounter
from app.models.users.customer import Customer
from app.views.customer import SearchIn, ReferencesOut, ItemsOut
from app.utils.auth import get_password_hash,create_access_token, verify_password
from app.utils.exceptions import ForbiddenException, UserNotFoundException

# TODO: Добавить загрузку файла

customer_router = APIRouter(tags=["Функции покупателя"])

@customer_router.get('/customer/reference')
async def get_references() -> ReferencesOut:
    references = await Customer.get_references()
    references = format_items(references)
    references = ReferencesOut(references=references)
    return references

@customer_router.get('/customer/item')
async def get_items() -> ItemsOut:
    items = await Customer.get_items()
    items = format_items(items)
    items = ItemsOut(items=items)
    return items

@customer_router.get('/producer/reference/search')
async def auto_link_item(search_in: SearchIn = Depends()) -> ReferencesOut:
    references = await Customer.references_search(search_in.search_query)
    return references

@customer_router.get('/customer/item/search')
async def search_items(search_in: SearchIn = Depends()) -> ItemsOut:
    items = await Customer.items_search(search_in.search_query)
    return items