from fastapi import APIRouter, status

router = APIRouter(prefix="/api", tags=["Metrics"])


@router.post("/metric", status_code=status.HTTP_201_CREATED)
async def create_metric(metric: dict):
    """
    Упрощённый приём метрик без проверки БД
    """
    print(f"📊 Получена метрика: {metric}")
    return {
        "message": "Metric recorded successfully",
        "sensor_id": metric.get("sensor_id"),
    }
