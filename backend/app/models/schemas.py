from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Схема для приёма данных от одного датчика
class MetricCreate(BaseModel):
    sensor_id: int = Field(..., description="ID датчика из БД")
    value: float = Field(..., description="Значение метрики (температура)")
    timestamp: Optional[datetime] = None  # Если не передано, используем текущее время

    class Config:
        json_schema_extra = {
            "example": {
                "sensor_id": 1,
                "value": 23.5,
                "timestamp": "2026-01-23T09:00:00",
            }
        }


# Схема для массовой загрузки (batch)
class MetricBatch(BaseModel):
    metrics: list[MetricCreate]


# Схема для ответа API (статистика)
class StatisticsResponse(BaseModel):
    sensor_id: int
    avg_value: float
    min_value: float
    max_value: float
    count: int
    period_start: datetime
    period_end: datetime


# Схема для информации о датчике (из PostgreSQL)
class SensorInfo(BaseModel):
    id: int
    name: str
    location: str
    sensor_type: str
    is_active: bool
