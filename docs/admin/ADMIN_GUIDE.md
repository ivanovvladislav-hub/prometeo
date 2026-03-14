# 🛠️ Prometeo - Руководство администратора

**Версия:** 1.0.0  
**Дата:** 26 января 2026  
**Аудитория:** Системные администраторы, DevOps

---

## 1. Системные требования

### 1.1. Минимальные требования

| Компонент | Минимум | Рекомендуется |
|-----------|---------|---------------|
| **CPU** | 2 ядра | 4 ядра |
| **RAM** | 4 GB | 8 GB |
| **Диск** | 20 GB SSD | 50 GB SSD |
| **ОС** | Ubuntu 20.04+ | Ubuntu 22.04 LTS |
| **Docker** | 25.0+ | Latest |
| **Docker Compose** | 2.24+ | Latest |

### 1.2. Сетевые требования

**Открытые порты:**
- `80` — HTTP (Frontend)
- `443` — HTTPS (при настройке SSL)
- `8000` — API (опционально, для прямого доступа)
- `5432` — PostgreSQL (только внутренняя сеть)
- `9000` — ClickHouse Native (только внутренняя сеть)
- `8123` — ClickHouse HTTP (для администрирования)

**Исходящие соединения:**
- Docker Hub (для скачивания образов)
- GitHub (если используется CI/CD)

---

## 2. Установка и развёртывание

### 2.1. Первоначальная установка

```bash
# 1. Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 2. Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. Перелогиньтесь для применения изменений
exit
# Затем войдите снова по SSH

# 4. Клонирование репозитория
git clone https://github.com/YOUR_ORG/prometeo.git
cd prometeo

# 5. Настройка переменных окружения
cp .env.example .env
nano .env  # Измените пароли!

# 6. Запуск системы
docker-compose up -d

# 7. Проверка статуса
docker-compose ps



# Создайте docker-compose.yml с образами из Docker Hub
version: '3.9'
services:
  backend:
    image: YOUR_USERNAME/prometeo-api:latest
    # ... остальная конфигурация
  
  frontend:
    image: YOUR_USERNAME/prometeo-frontend:latest
    # ... остальная конфигурация



3. Конфигурация
3.1. Переменные окружения (.env)
Обязательные параметры:

env
# PostgreSQL
POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD
POSTGRES_USER=prometeo_user
POSTGRES_DB=prometeo_meta

# ClickHouse (оставьте пустым для режима без пароля)
CLICKHOUSE_PASSWORD=

# Таймзона
TZ=Europe/Moscow
Генерация безопасных паролей:

bash
# PostgreSQL пароль
openssl rand -base64 32

# Пример: vK8Zx2mP4nQ7sT1wY5eR3aU6bN9cV0dX
3.2. Настройка Nginx (SSL/TLS)
Для production среды настройте HTTPS:

bash
# 1. Установка Certbot
sudo apt install certbot python3-certbot-nginx

# 2. Получение сертификата
sudo certbot --nginx -d prometeo.your-domain.com

# 3. Автообновление сертификата
sudo systemctl enable certbot.timer
3.3. Ограничение ресурсов
Отредактируйте docker-compose.yml:

yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'        # Максимум 2 ядра
          memory: 1G       # Максимум 1GB RAM
        reservations:
          cpus: '0.5'      # Минимум 0.5 ядра
          memory: 256M     # Минимум 256MB
4. Управление системой
4.1. Основные команды
bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Перезапуск конкретного сервиса
docker-compose restart backend

# Просмотр логов
docker-compose logs -f                # Все сервисы
docker-compose logs -f backend        # Только backend
docker-compose logs -f --tail=100 backend  # Последние 100 строк

# Проверка статуса
docker-compose ps

# Обновление образов
docker-compose pull
docker-compose up -d
4.2. Мониторинг ресурсов
bash
# Использование ресурсов контейнерами
docker stats

# Использование диска
docker system df

# Подробная информация о контейнере
docker inspect prometeo-api
5. Обслуживание баз данных
5.1. PostgreSQL
Создание бэкапа:

bash
# Автоматический бэкап (добавьте в cron)
docker exec prometeo-postgres pg_dump -U prometeo_user prometeo_meta > backup_$(date +%Y%m%d).sql

# Бэкап с сжатием
docker exec prometeo-postgres pg_dump -U prometeo_user prometeo_meta | gzip > backup_$(date +%Y%m%d).sql.gz
Восстановление из бэкапа:

bash
# Восстановление
docker exec -i prometeo-postgres psql -U prometeo_user prometeo_meta < backup_20260126.sql

# Из сжатого архива
gunzip -c backup_20260126.sql.gz | docker exec -i prometeo-postgres psql -U prometeo_user prometeo_meta
Подключение к базе:

bash
docker exec -it prometeo-postgres psql -U prometeo_user -d prometeo_meta
Полезные SQL запросы:

sql
-- Список датчиков
SELECT * FROM sensors WHERE is_active = true;

-- Количество датчиков по типам
SELECT sensor_type, COUNT(*) FROM sensors GROUP BY sensor_type;

-- Размер базы данных
SELECT pg_size_pretty(pg_database_size('prometeo_meta'));

-- Активные подключения
SELECT count(*) FROM pg_stat_activity;
5.2. ClickHouse
Создание бэкапа:

bash
# Подключение
docker exec -it prometeo-clickhouse clickhouse-client

# Экспорт данных
SELECT * FROM metrics 
INTO OUTFILE '/var/lib/clickhouse/backup_metrics.csv' 
FORMAT CSV;
Очистка старых данных:

sql
-- Удаление данных старше 90 дней
ALTER TABLE metrics DELETE WHERE timestamp < now() - INTERVAL 90 DAY;

-- Оптимизация таблицы после удаления
OPTIMIZE TABLE metrics FINAL;
Мониторинг производительности:

sql
-- Размер таблицы
SELECT 
    formatReadableSize(sum(bytes)) as size,
    count() as parts
FROM system.parts
WHERE table = 'metrics' AND active;

-- Статистика по партициям
SELECT 
    partition,
    count() as parts,
    formatReadableSize(sum(bytes)) as size
FROM system.parts
WHERE table = 'metrics' AND active
GROUP BY partition
ORDER BY partition DESC;
6. Мониторинг и логирование
6.1. Логи приложения
Просмотр логов:

bash
# Все логи
docker-compose logs -f

# Фильтрация ошибок
docker-compose logs backend | grep ERROR

# Экспорт логов в файл
docker-compose logs --since 24h > logs_$(date +%Y%m%d).txt
6.2. Health Checks
Проверка здоровья сервисов:

bash
# Через curl
curl http://localhost:8000/health
curl http://localhost/

# Через Docker
docker ps --filter "health=healthy"
6.3. Настройка мониторинга (опционально)
Интеграция с Prometheus + Grafana:

yaml
# Добавить в docker-compose.yml
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
7. Обновление системы
7.1. Обновление без простоя
bash
# 1. Скачиваем новые образы
docker-compose pull

# 2. Пересоздаём контейнеры (без удаления данных!)
docker-compose up -d --no-deps --build backend frontend

# 3. Проверяем статус
docker-compose ps
docker-compose logs -f backend
7.2. Откат к предыдущей версии
bash
# 1. Останавливаем текущие контейнеры
docker-compose down

# 2. Изменяем версию в docker-compose.yml
# image: prometeo-api:v1.0.0  # вместо :latest

# 3. Запускаем
docker-compose up -d
8. Безопасность
8.1. Checklist безопасности
✅ Изменены все пароли по умолчанию в .env

✅ PostgreSQL и ClickHouse доступны только из внутренней сети Docker

✅ Настроен HTTPS с валидным SSL сертификатом

✅ Включен firewall (ufw/iptables)

✅ Регулярные бэкапы (автоматизированы через cron)

✅ Логи ротируются (не занимают весь диск)

✅ Обновления безопасности ОС применяются еженедельно

8.2. Настройка Firewall
bash
# Установка UFW
sudo apt install ufw

# Разрешаем SSH
sudo ufw allow 22/tcp

# Разрешаем HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Включаем firewall
sudo ufw enable
sudo ufw status
8.3. Ограничение доступа к базам данных
В docker-compose.yml удалите публикацию портов для production:

yaml
# ПЛОХО (для разработки):
postgres:
  ports:
    - "5432:5432"  # Доступен извне!

# ХОРОШО (для production):
postgres:
  expose:
    - 5432  # Доступен только внутри Docker network
9. Автоматизация обслуживания
9.1. Cron задачи
bash
# Редактируем crontab
crontab -e

# Добавляем задачи:

# Бэкап PostgreSQL каждый день в 02:00
0 2 * * * cd ~/prometeo && docker exec prometeo-postgres pg_dump -U prometeo_user prometeo_meta | gzip > /backups/prometeo_$(date +\%Y\%m\%d).sql.gz

# Очистка старых бэкапов (старше 30 дней)
0 3 * * * find /backups -name "prometeo_*.sql.gz" -mtime +30 -delete

# Очистка Docker (неиспользуемые образы)
0 4 * * 0 docker system prune -af --volumes

# Проверка обновлений
0 5 * * * cd ~/prometeo && git pull && docker-compose pull
9.2. Скрипт автоматического восстановления
bash
nano ~/prometeo/scripts/auto-restart.sh
bash
#!/bin/bash
# Скрипт проверки и автоматического перезапуска

cd ~/prometeo

# Проверяем health endpoint
if ! curl -sf http://localhost:8000/health > /dev/null; then
    echo "[$(date)] API не отвечает. Перезапуск..." >> /var/log/prometeo-restart.log
    docker-compose restart backend
    sleep 10
fi

# Проверяем frontend
if ! curl -sf http://localhost/ > /dev/null; then
    echo "[$(date)] Frontend не отвечает. Перезапуск..." >> /var/log/prometeo-restart.log
    docker-compose restart frontend
fi
bash
chmod +x ~/prometeo/scripts/auto-restart.sh

# Добавляем в cron (каждые 5 минут)
*/5 * * * * ~/prometeo/scripts/auto-restart.sh
10. Troubleshooting
10.1. Контейнер не запускается
bash
# Смотрим подробные логи
docker-compose logs backend

# Проверяем конфигурацию
docker-compose config

# Проверяем ресурсы
docker stats
free -h
df -h
10.2. База данных недоступна
bash
# Проверяем статус
docker ps | grep postgres

# Проверяем логи PostgreSQL
docker logs prometeo-postgres

# Тестируем подключение
docker exec prometeo-postgres pg_isready -U prometeo_user
10.3. Высокая нагрузка
bash
# Проверяем какой сервис потребляет ресурсы
docker stats

# Проверяем количество подключений к PostgreSQL
docker exec prometeo-postgres psql -U prometeo_user -d prometeo_meta -c "SELECT count(*) FROM pg_stat_activity;"

# Проверяем размер данных в ClickHouse
docker exec prometeo-clickhouse clickhouse-client --query "SELECT formatReadableSize(sum(bytes)) FROM system.parts WHERE active;"
11. Контакты и поддержка
Команда разработки:

Email: devops@your-company.com

GitHub: https://github.com/YOUR_ORG/prometeo

Documentation: https://prometeo.readthedocs.io

Экстренные контакты:

On-call: +7 (XXX) XXX-XX-XX (24/7)

© 2026 Prometeo Team. Internal Use Only.
