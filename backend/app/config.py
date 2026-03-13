from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    # ClickHouse
    clickhouse_host: str
    clickhouse_port: int
    clickhouse_db: str

    # Настройки приложения
    app_title: str = "Prometeo API"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
