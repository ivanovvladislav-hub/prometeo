from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Statistics"])


@router.get("/test")
async def test():
    return {"message": "API работает"}


@router.get("/sensors")
async def get_all_sensors():
    """Временная заглушка для тестов CI/CD"""
    return {
        "sensors": [
            {
                "id": 1,
                "name": "Sensor-001",
                "location": "Server Room A",
                "sensor_type": "temperature",
                "is_active": True,
            },
            {
                "id": 2,
                "name": "Sensor-002",
                "location": "Office Floor 2",
                "sensor_type": "temperature",
                "is_active": True,
            },
            {
                "id": 3,
                "name": "Sensor-003",
                "location": "Data Center",
                "sensor_type": "temperature",
                "is_active": True,
            },
        ]
    }
