from app.services.mongo import Mongo

async def match_item(item: dict) -> str | None:
    reference = await Mongo.db['references'].find_one({'$text': {'$search': item['name']}},
                                                      projection={'score': {'$meta': "textScore"}},
                                                      sort=[('score', {'$meta': "textScore"}), ],
                                                      limit=1)
    if reference:
        return reference['product_id']
    else:
        return None