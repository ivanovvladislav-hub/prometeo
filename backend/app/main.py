from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.models.database import init_postgres, close_postgres
from app.routers import metrics, stats  # добавил metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения:
    - startup: подключение к БД
    - shutdown: закрытие соединений
    """
    # Startup
    print("🚀 Starting Prometeo API...")
    await init_postgres()
    # init_clickhouse() - временно отключено
    print("✅ All systems ready!")

    yield

    # Shutdown
    print("🛑 Shutting down...")
    await close_postgres()
    # close_clickhouse() - временно отключено
    print("👋 Goodbye!")


# Создание приложения FastAPI
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="API для сбора и аналитики метрик с IoT-датчиков",
    lifespan=lifespan,
)

# CORS middleware (чтобы фронтенд мог обращаться к API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретный домен!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(metrics.router)  # включено
app.include_router(stats.router)  # включено


# Главная страница (проверка работоспособности)
@app.get("/")
async def root():
    return {
        "message": "Prometeo API is running",
        "version": settings.app_version,
        "docs": "/docs",
    }


# Health check эндпоинт (для мониторинга)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
