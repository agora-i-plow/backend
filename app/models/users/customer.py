from app.services.mongo import Mongo


class Customer:
    @classmethod
    async def get_references(cls) -> list[dict]:
        references = list()
        async for reference in Mongo.db["references"].find():
            references.append(reference)
        return references

    @classmethod
    async def get_items(cls) -> list[dict]:
        items = list()
        async for item in Mongo.db["items"].find():
            items.append(item)
        return items

    @classmethod
    async def references_search(cls, query: str) -> list[dict]:
        references = list()
        async for reference in Mongo.db["references"].find(
            {"$text": {"$search": query}}
        ):
            references.append(reference)
        return references

    @classmethod
    async def items_search(cls, query: str) -> list[dict]:
        items = list()
        async for item in Mongo.db["items"].find({"$text": {"$search": query}}):
            items.append(item)
        return items
