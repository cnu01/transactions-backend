from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    mongodb_url: str = Field(default="mongodb://localhost:27017")
    database_name: str = Field(default="transaction_service")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
