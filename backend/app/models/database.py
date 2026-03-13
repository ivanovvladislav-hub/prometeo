import asyncpg
from clickhouse_driver import Client
from app.config import settings

# Пул подключений к PostgreSQL
postgres_pool = None

async def init_postgres():
    global postgres_pool
    postgres_pool = await asyncpg.create_pool(
        host=settings.postgres_host,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        database=settings.postgres_db,
        min_size=5,
        max_size=20
    )
    print("✅ PostgreSQL connection pool created")

async def close_postgres():
    global postgres_pool
    if postgres_pool:
        await postgres_pool.close()
        print("❌ PostgreSQL connection pool closed")

# Клиент ClickHouse (синхронный) - временно отключен
# clickhouse_client = None

# def init_clickhouse():
#     global clickhouse_client
#     clickhouse_client = Client(
#         host=settings.clickhouse_host,
#         port=settings.clickhouse_port,
#         database=settings.clickhouse_db
#     )
#     # Проверяем подключение
#     result = clickhouse_client.execute("SELECT 1")
#     print(f"✅ ClickHouse connected: {result}")

# def close_clickhouse():
#     global clickhouse_client
#     if clickhouse_client:
#         clickhouse_client.disconnect()
#         print("❌ ClickHouse disconnected")
