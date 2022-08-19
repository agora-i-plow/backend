import asyncpg
from asyncpg import Record
from app.utils.exceptions import InternalServerError
from app.utils.get_settings import get_postgres_settings
from app.utils.logger import Log

class Postgres:
    pool: asyncpg.Pool = None

    @classmethod
    async def connect_db(cls) -> None:
        try:
            cls.pool = await asyncpg.create_pool(get_postgres_settings().db_uri)
        except Exception as e:
            raise InternalServerError(e) from e

    @classmethod
    async def execute(cls, sql, *args) -> None:
        async with cls.pool.acquire() as con:
            await Log.log_database_query('execute', sql, args)
            await con.execute(sql, *args)

    @classmethod
    async def fetch(cls, sql, *args) -> list[Record]:
        async with cls.pool.acquire() as con:
            await Log.log_database_query('fetch', sql, args)
            result = await con.fetch(sql, *args)
        return result

    @classmethod
    async def fetchval(cls, sql, *args) -> list:
        async with cls.pool.acquire() as con:
            await Log.log_database_query('fetchval', sql, args)
            result = await con.fetchval(sql, *args)
        return result

    @classmethod
    async def fetchrow(cls, sql, *args) -> Record:
        async with cls.pool.acquire() as con:
            await Log.log_database_query('fetchrow', sql, args)
            result = await con.fetchrow(sql, *args)
        return result

    @classmethod
    async def disconnect_db(cls) -> None:
        await cls.pool.close()
