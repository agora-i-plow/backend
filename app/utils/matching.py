from app.services.mongo import Mongo

async def match_item(item: dict) -> str | None:
    item = reformat_item(item)
    reference = await Mongo.db['references'].find_one({'$text': {'$search': item['combined']}},
                                                      projection={'score': {'$meta': "textScore"}},
                                                      sort=[('score', {'$meta': "textScore"}), ],
                                                      limit=1)
    if reference:
        return reference['product_id']
    else:
        return None


def reformat_item(item: dict) -> dict:
    props = ' '.join(item['props'])
    props = ' '.join([props, item['name']])
    item['combined'] = props
    return item


async def reformat_references() -> None:
    errors = 0
    async for item in Mongo.db['references'].find():
        try:
            new_item = reformat_item(item)
            await Mongo.db['references'].delete_many({'product_id': item['product_id']})
            await Mongo.db['references'].insert_one(new_item)
        except Exception as e:
            errors += 1
    print(errors)