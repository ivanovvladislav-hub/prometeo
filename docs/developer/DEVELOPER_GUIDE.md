# 💻 Prometeo - Руководство разработчика

**Версия:** 1.0.0  
**Аудитория:** Backend/Frontend разработчики

---

## 1. Архитектура системы

### 1.1. Общая схема
┌─────────────┐
│ Датчики │ IoT Devices / Data Generators
└──────┬──────┘
│ HTTP POST
▼
┌─────────────┐
│ Nginx │ Reverse Proxy + Static Files
└──────┬──────┘
│
├─────────────────┐
│ │
▼ ▼
┌─────────────┐ ┌─────────────┐
│ Frontend │ │ Backend │
│ (Static) │ │ (FastAPI) │
└─────────────┘ └──────┬──────┘
│
┌─────────────┴─────────────┐
▼ ▼
┌────────────────────┐ ┌────────────────────┐
│ PostgreSQL │ │ ClickHouse │
│ (Metadata) │ │ (Metrics) │
└────────────────────┘ └────────────────────┘

text

### 1.2. Стек технологий

**Backend:**
- Python 3.11
- FastAPI 0.109.0 (асинхронный веб-фреймворк)
- asyncpg (PostgreSQL async driver)
- clickhouse-driver (ClickHouse client)
- Pydantic (валидация данных)
- Uvicorn (ASGI сервер)

**Frontend:**
- HTML5/CSS3 (Vanilla, без фреймворков)
- JavaScript ES6+ (async/await, fetch API)
- Chart.js 4.4.1 (визуализация)
- Nginx (веб-сервер)

**Инфраструктура:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- PostgreSQL 16 (метаданные)
- ClickHouse 24.1 (time-series данные)

---

## 2. Настройка окружения для разработки

### 2.1. Backend Development

```bash
# Клонирование репозитория
git clone https://github.com/YOUR_ORG/prometeo.git
cd prometeo/backend

# Создание виртуального окружения
python3.11 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Запуск PostgreSQL и ClickHouse локально
docker-compose up -d postgres clickhouse

# Запуск API в режиме разработки
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Hot reload включен — изменения в коде применяются автоматически!

2.2. Frontend Development
bash
# Установка Live Server (опционально)
npm install -g live-server

# Запуск локального сервера
cd prometeo/frontend
live-server --port=3000 --host=0.0.0.0

# Или просто откройте index.html в браузере
Примечание: Для работы с API измените API_BASE_URL в js/app.js:

javascript
const API_BASE_URL = 'http://localhost:8000/api';
3. Структура проекта
text
prometeo/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Точка входа FastAPI
│   │   ├── config.py               # Конфигурация (pydantic-settings)
│   │   ├── models/
│   │   │   ├── database.py        # Подключения к БД
│   │   │   └── schemas.py         # Pydantic схемы
│   │   ├── routers/
│   │   │   ├── metrics.py         # POST /api/metric, /api/metrics/batch
│   │   │   └── stats.py           # GET /api/stats, /api/timeseries
│   │   └── services/
│   │       ├── clickhouse_service.py  # Логика работы с ClickHouse
│   │       └── postgres_service.py    # Логика работы с PostgreSQL
│   ├── tests/
│   │   └── test_main.py           # Unit тесты
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── frontend/
│   ├── index.html                 # Главная страница
│   ├── css/
│   │   └── style.css             # Стили
│   ├── js/
│   │   ├── app.js                # Основная логика
│   │   └── chart-config.js       # Конфигурация Chart.js
│   ├── Dockerfile
│   └── nginx.conf
│
├── testing/
│   ├── locustfile.py             # Нагрузочные тесты (Locust)
│   └── async_generator.py        # Генератор данных
│
├── init-scripts/
│   ├── init-postgres.sql         # Инициализация PostgreSQL
│   └── init-clickhouse.sql       # Инициализация ClickHouse
│
├── .github/
│   └── workflows/
│       ├── ci-tests.yml          # CI Pipeline
│       └── cd-deploy.yml         # CD Pipeline
│
├── docs/
│   ├── user/USER_GUIDE.md
│   ├── admin/ADMIN_GUIDE.md
│   └── developer/DEVELOPER_GUIDE.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
4. API Endpoints
4.1. Metric Ingestion
POST /api/metric

Принимает одну метрику от датчика.

Request:

json
{
  "sensor_id": 1,
  "value": 23.5,
  "timestamp": "2026-01-26T09:00:00"  // optional
}
Response (201):

json
{
  "message": "Metric recorded successfully",
  "sensor_id": 1
}
POST /api/metrics/batch

Массовая отправка метрик (оптимизация).

Request:

json
{
  "metrics": [
    {"sensor_id": 1, "value": 23.5},
    {"sensor_id": 2, "value": 21.2},
    {"sensor_id": 1, "value": 23.7}
  ]
}
Response (201):

json
{
  "message": "Batch recorded successfully",
  "count": 3
}
4.2. Data Retrieval
GET /api/stats/{sensor_id}?hours=24

Возвращает агрегированную статистику.

Response (200):

json
{
  "sensor_id": 1,
  "avg_value": 22.5,
  "min_value": 20.1,
  "max_value": 25.3,
  "count": 1234,
  "period_start": "2026-01-25T09:00:00",
  "period_end": "2026-01-26T09:00:00"
}
GET /api/timeseries/{sensor_id}?hours=24&interval=5

Временной ряд для графика.

Response (200):

json
{
  "sensor_id": 1,
  "sensor_name": "Sensor-001",
  "data": [
    {"timestamp": "2026-01-26T08:00:00", "value": 22.5},
    {"timestamp": "2026-01-26T08:05:00", "value": 22.7},
    ...
  ]
}
GET /api/sensors

Список всех датчиков.

Response (200):

json
{
  "sensors": [
    {
      "id": 1,
      "name": "Sensor-001",
      "location": "Server Room A",
      "sensor_type": "temperature",
      "is_active": true
    },
    ...
  ]
}
5. Работа с базами данных
5.1. PostgreSQL Schema
sql
-- Таблица датчиков
CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    sensor_type VARCHAR(50) DEFAULT 'temperature',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
5.2. ClickHouse Schema
sql
-- Таблица метрик (time-series)
CREATE TABLE metrics (
    timestamp DateTime,
    sensor_id UInt32,
    value Float64
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (sensor_id, timestamp);
Партиционирование: Данные разделяются по месяцам для оптимизации запросов и удаления старых данных.



6. Тестирование
6.1. Запуск Unit тестов
bash
cd backend
pytest tests/ -v --cov=app
6.2. Запуск нагрузочных тестов
bash
cd testing
locust -f locustfile.py --host=http://localhost:8000
Откройте http://localhost:8089 и запустите тест.

6.3. Написание новых тестов
Пример теста для нового endpoint:

python
def test_new_endpoint():
    response = client.get("/api/new-endpoint")
    assert response.status_code == 200
    assert "expected_field" in response.json()
7. Добавление нового функционала
7.1. Добавление нового API endpoint
Шаг 1: Создайте Pydantic схему в models/schemas.py:

python
class NewFeatureRequest(BaseModel):
    field1: str
    field2: int
Шаг 2: Создайте роутер в routers/new_feature.py:

python
from fastapi import APIRouter
router = APIRouter(prefix="/api", tags=["NewFeature"])

@router.post("/new-endpoint")
async def create_something(data: NewFeatureRequest):
    # Ваша логика
    return {"status": "success"}
Шаг 3: Зарегистрируйте роутер в main.py:

python
from app.routers import new_feature
app.include_router(new_feature.router)
7.2. Добавление миграции БД
sql
-- Создайте файл: init-scripts/migration_001.sql
ALTER TABLE sensors ADD COLUMN description TEXT;
Примените:

bash
docker exec -i prometeo-postgres psql -U prometeo_user -d prometeo_meta < init-scripts/migration_001.sql
8. Git Workflow
8.1. Branching Strategy
text
main (production)
  └── develop (staging)
       ├── feature/add-alerts
       ├── feature/export-api
       └── bugfix/chart-rendering
8.2. Процесс разработки
bash
# 1. Создайте feature branch
git checkout -b feature/my-awesome-feature

# 2. Внесите изменения и коммитьте
git add .
git commit -m "feat: Add awesome feature"

# 3. Пушьте в GitHub
git push origin feature/my-awesome-feature

# 4. Создайте Pull Request на GitHub
# 5. После code review и прохождения CI — мержите в develop
# 6. Периодически develop мержится в main для релизов
8.3. Commit Message Convention
Используем Conventional Commits:

text
feat: новая функциональность
fix: исправление бага
docs: изменения в документации
style: форматирование кода
refactor: рефакторинг
test: добавление тестов
chore: обновление зависимостей, CI и т.д.
Примеры:

bash
git commit -m "feat: Add real-time WebSocket updates"
git commit -m "fix: Correct timezone handling in stats endpoint"
git commit -m "docs: Update API documentation"
9. Code Style
9.1. Python (Backend)
Используем Black для форматирования:

bash
black app/
Используем isort для сортировки импортов:

bash
isort app/
Проверка кода с flake8:

bash
flake8 app/ --max-line-length=127
9.2. JavaScript (Frontend)
Используйте ES6+ синтаксис

Предпочитайте const и let вместо var

Асинхронность через async/await, а не callbacks

Комментарии для сложной логики

Пример:

javascript
// ✅ Хорошо
async function loadData() {
    const response = await fetch('/api/sensors');
    const data = await response.json();
    return data;
}

// ❌ Плохо
function loadData() {
    fetch('/api/sensors').then(function(response) {
        return response.json();
    }).then(function(data) {
        console.log(data);
    });
}
10. Полезные команды для разработки
bash
# Пересборка только backend после изменений
docker-compose up -d --no-deps --build backend

# Подключение к базе PostgreSQL
docker exec -it prometeo-postgres psql -U prometeo_user -d prometeo_meta

# Подключение к ClickHouse
docker exec -it prometeo-clickhouse clickhouse-client

# Просмотр логов в реальном времени
docker-compose logs -f backend

# Очистка Docker кэша (если проблемы со сборкой)
docker system prune -a

# Форматирование всего Python кода
cd backend && black . && isort .
11. Debugging
11.1. Backend
Добавьте в код:

python
import ipdb; ipdb.set_trace()  # Breakpoint
Запустите без Docker:

bash
uvicorn app.main:app --reload
11.2. Frontend
Используйте Browser DevTools (F12):

Console — ошибки JavaScript

Network — HTTP запросы

Sources — debugging JavaScript

12. Контакты
Tech Lead: tech-lead@your-company.com
Code Review: Создавайте Pull Requests в GitHub
Questions: Используйте GitHub Discussions


