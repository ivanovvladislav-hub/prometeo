# Changelog

Все значимые изменения в проекте Prometeo будут задокументированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
и проект следует [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Планируется
- Аутентификация пользователей (JWT)
- WebSocket для real-time обновлений
- Email уведомления о критических значениях
- Мобильное приложение

## [1.0.0] - 2026-01-26

### Added
- Полнофункциональный REST API на FastAPI
- Веб-дашборд с интерактивными графиками (Chart.js)
- Поддержка PostgreSQL для метаданных
- Поддержка ClickHouse для time-series данных
- Docker Compose для оркестрации
- CI/CD pipeline через GitHub Actions
- Автоматическое тестирование (unit, integration)
- Нагрузочное тестирование с Locust
- Полная документация (User/Admin/Developer Guides)
- Health checks для всех сервисов
- Автоматическая публикация в Docker Hub

### Performance
- API выдерживает 500+ req/sec
- Хранение 1M+ метрик без деградации
- Latency (95th percentile) < 50ms

### Security
- Непривилегированные пользователи в Docker
- Изоляция сетей в Docker Compose
- Health checks для автовосстановления
- Secrets management через GitHub Secrets

## [0.3.0] - 2026-01-23 (Спринт 4)

### Added
- Интеграция API и Frontend
- Стресс-тестирование системы
- Генераторы нагрузки (синхронный и асинхронный)
- Locust сценарии тестирования

## [0.2.0] - 2026-01-20 (Спринт 3)

### Added
- Разработка бэкенда на FastAPI
- Интеграция с PostgreSQL и ClickHouse
- Генератор тестовых данных

## [0.1.0] - 2026-01-15 (Спринт 2)

### Added
- Проектирование архитектуры
- UML диаграммы
- ER-диаграммы БД
- UI/UX макеты в Figma

## [0.0.1] - 2026-01-10 (Спринт 1)

### Added
- Настройка виртуальной инфраструктуры
- Установка Linux, Docker
- Конфигурация сети
- Базовая настройка Nginx
