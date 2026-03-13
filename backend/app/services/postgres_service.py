from app.models.database import postgres_pool
from app.models.schemas import SensorInfo

class PostgresService:
    
    @staticmethod
    async def get_sensor_by_id(sensor_id: int):
        """Получить информацию о датчике"""
        async with postgres_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, name, location, sensor_type, is_active FROM sensors WHERE id = $1",
                sensor_id
            )
            if row:
                return SensorInfo(**dict(row))
            return None
    
    @staticmethod
    async def get_all_sensors():
        """Получить список всех активных датчиков"""
        async with postgres_pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, name, location, sensor_type, is_active FROM sensors WHERE is_active = true"
            )
            return [SensorInfo(**dict(row)) for row in rows]
    
    @staticmethod
    async def sensor_exists(sensor_id: int):
        """Проверка существования датчика"""
        async with postgres_pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM sensors WHERE id = $1 AND is_active = true)",
                sensor_id
            )
            return result
