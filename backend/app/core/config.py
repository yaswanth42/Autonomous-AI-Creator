import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "AutoPersona AI"
    APP_ENV: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./autopersona.db"

    # AI & Search Providers
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    TAVILY_API_KEY: str = ""

    # Autonomous Persona
    PERSONA_NAME: str = "Ada"
    PERSONA_DOMAIN: str = "AI Security"
    DEFAULT_EDITORIAL_THRESHOLD: float = 7.0
    SCHEDULER_INTERVAL_HOURS: int = 4
    TOPIC_SEARCH_INTERVAL_HOURS: int = 1

    # Breeth Memory
    BREETH_MEMORY_MAX_ITEMS: int = 5000
    BREETH_SIMILARITY_THRESHOLD: float = 0.82

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
