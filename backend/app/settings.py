from pydantic_settings import BaseSettings
from pydantic import SecretStr
from datetime import timedelta
import os

class ApplicationSettings(BaseSettings):
    """Application settings class"""
    DATABASE_URL: str = 'sqlite:///./app.db'
    SECRET_KEY: SecretStr = os.environ.get('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ALGORITHM: str = 'HS256' 
    ACCESS_TOKEN_EXPIRE_TIME: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)