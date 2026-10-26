from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Default TRUE so MVP runs without PostgreSQL/Docker on constrained machines
    demo_mode: bool = True
    database_url: str = "postgresql+psycopg2://dwh_admin:dwh_secret_change_me@localhost:5432/bbsb_dwh"
    jwt_secret: str = "change-me-in-production-use-long-random"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    cors_origins: str = "http://localhost:3000"


settings = Settings()
