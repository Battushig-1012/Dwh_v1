from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://dwh_admin:dwh_secret_change_me@localhost:5432/bbsb_dwh"
    core_db_url: str | None = None
    erp_db_url: str | None = None
    loan_app_api_url: str = "http://localhost:9000"
    use_demo_sources: bool = True


settings = Settings()
