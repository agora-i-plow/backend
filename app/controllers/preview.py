import asyncio

from fastapi import APIRouter, Body

from app.utils.matching import match_item

preview_router = APIRouter(tags=["Превью метчера"])

# TODO: Написать где-то, что тут логика изолирована от бд в угоду скорости


@preview_router.post(
    "/match_products",
    responses={
        200: {
            "description": "List of dicts containing item id and matched reference id",
            "content": {
                "application/json": {
                    "example": [
                        {"id": "0039af5efceac4ab", "reference_id": "28085e941cde1639"},
                        {"id": "004f2158acb8165c", "reference_id": "9afe55bb4bf1e8a8"},
                    ]
                }
            },
        }
    },
)
async def upload_items_with_matching(
    items: list[dict] = Body(
        ...,
        example=[
            {
                "id": "0039af5efceac4ab",
                "name": "Холодильник Бирюса 118",
                "props": ["Мощность  замораживания  4 кг/сутки"],
            },
            {
                "id": "004f2158acb8165c",
                "name": "ASUS TUF-GTX1660S-O6G-GAMING Видеокарта",
                "props": [
                    "Объем  видеопамяти\t6144 МБ",
                    "Частота  памяти\t14002 МГц",
                    "Разъемы   и интерфейсы выход DVI, выход DisplayPort, выход HDMI",
                ],
            },
        ],
    )
) -> list[dict[str, str]]:
    async def converter(item):
        reference_id = await match_item(item)
        return {"id": item["id"], "reference_id": reference_id}

    matched: list[dict[str, str]] = list()
    coroutines = list()
    for item in items:
        coroutines.append(converter(item))
    matched = await asyncio.gather(*coroutines)
    return matched
