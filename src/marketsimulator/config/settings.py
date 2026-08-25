from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "marketsimulator"
    environment: str = "development"
    log_level: str = "INFO"
    kafka_bootstrap_servers: str = "kafka:29092"
    kafka_topic: str = "trades"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
