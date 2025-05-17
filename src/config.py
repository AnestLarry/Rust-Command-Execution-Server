from pydantic import AnyUrl
from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class Settings(BaseSettings):
    DB_ENGINE: str = "sqlite"
    DB_URL: AnyUrl = "sqlite:///./rces.db"
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        # env_file = ".env" # No longer needed as we load explicitly
        env_file_encoding = "utf-8"

settings = Settings()
