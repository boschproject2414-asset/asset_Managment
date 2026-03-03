from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Asset Management System'
    api_v1_prefix: str = '/api/v1'
    secret_key: str = 'change-this-secret-key'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 480

    database_url: str = 'postgresql+psycopg2://postgres:postgres@localhost:5432/asset_management'


settings = Settings()
