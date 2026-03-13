import asyncpg
from clickhouse_driver import Client

from app.config import settings

# Пул подключений к PostgreSQL
postgres_pool = None


async def init_postgres():
    postgres_pool = await asyncpg.create_pool(
        host=settings.postgres_host,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        database=settings.postgres_db,
        min_size=5,
        max_size=20,
    )
    print("✅ PostgreSQL connection pool created")


async def close_postgres():
    if postgres_pool:
        await postgres_pool.close()
        print("❌ PostgreSQL connection pool closed")
