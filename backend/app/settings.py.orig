from pydantic_settings import BaseSettings
from pydantic import SecretStr
from datetime import timedelta

class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite:///./app.db'
    SECRET_KEY: SecretStr = 'dev-secret-key-change-in-production'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ALGORITHM: str = 'HS256'