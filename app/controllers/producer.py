from fastapi import APIRouter
from fastapi.param_functions import Depends

from app.models.users.producer import Producer
from app.utils.file_parser import parse_json_file
from app.views.admin import DuplicatesCounter
from app.views.common import FileIn, SuccessfullResponse, UserIn
from app.views.producer import ItemIn

producer_router = APIRouter(tags=["Функции производителя"])


@producer_router.post("/producer/upload")
async def upload_items(
    items: list[dict], user_in: UserIn = Depends()
) -> DuplicatesCounter:
    producer = await Producer.get(user_in.username)
    duplicates = await producer.upload_items(items)
    return DuplicatesCounter(duplicates=duplicates)


@producer_router.post("/producer/upload/file")
async def upload_items_using_file(
    file_in: FileIn = Depends(), user_in: UserIn = Depends()
) -> DuplicatesCounter:
    producer = await Producer.get(user_in.username)
    items = parse_json_file(file_in.file)
    duplicates = await producer.upload_items(items)
    return DuplicatesCounter(duplicates=duplicates)


@producer_router.post("/producer/link/manual")
async def manually_link_item(
    item_in: ItemIn, reference_in: ItemIn, user_in: UserIn = Depends()
) -> SuccessfullResponse:
    producer = await Producer.get(user_in.username)
    await producer.manually_link(item_in.product_id, reference_in.product_id)
    return SuccessfullResponse()


@producer_router.post("/producer/link/auto")
async def auto_link_item(
    item_in: ItemIn, user_in: UserIn = Depends()
) -> SuccessfullResponse:
    producer = await Producer.get(user_in.username)
    await producer.auto_link(item_in.product_id)
    return SuccessfullResponse()
