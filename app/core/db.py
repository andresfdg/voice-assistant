import asyncpg

from app.core.config import settings

database_pool = None


async def init_db():

    global database_pool
    if not database_pool:

        database_pool = await asyncpg.create_pool(
            user=f"{settings.DB_USER}",
            password=f"{settings.DB_PASSWORD}",
            host=f"{settings.DB_HOST}",
            port=f"{settings.DB_PORT}",
            database=f"{settings.DB_NAME}",
        )


async def close_db():

    global database_pool
    if database_pool:
        await database_pool.close()
        database_pool = None


async def get_db():

    global database_pool
    if not database_pool:
        raise Exception("The database has not been initialized.")
    return database_pool
