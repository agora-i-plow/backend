from time import perf_counter
from pprint import pp
from json import dump
import asyncio
from app.services.mongo import Mongo
from app.utils.matching import match_item
from app.utils.formatter import format_item

from pprint import pprint

erroneous_references = {}

async def main():
    Mongo.connect_db()
    good = 0
    total = 0
    skips = 0


    async for item in Mongo.db['items'].find(limit=2780):
        new_item = format_item(item)
        reference = await match_item(new_item)
        try:
            add = 1 if reference == item['reference_id'] else 0
            good += add
            if reference is None or add == 0:
                ref_obj = await Mongo.db['references'].find_one({'product_id':reference})

                if reference not in erroneous_references:
                    erroneous_references[reference] = 1
                erroneous_references[reference] += 1
                # print(f"bad object: {ref_obj}, {item}")
                # ref_item_obj = await Mongo.db['references'].find_one({'product_id':item['reference_id']})
                # pprint(ref_obj)
                # pprint(ref_item_obj)
                # pprint(item)

                # print("="*50)

            total += 1
        except TypeError as e:
            print(f"TypeError: {e}")
            skips += 1
    Mongo.disconnect_db()
    pp({
        'good': good,
        'total': total,
        'skips': skips,
        'accuracy': good/total
    })
t_start = perf_counter()
asyncio.run(main())
print(perf_counter()-t_start,'seconds')
print('='*50)

# pprint(erroneous_references)

# Print sorted dictionary by value
# pprint(sorted(erroneous_references.items(), key=lambda x: x[1]))
