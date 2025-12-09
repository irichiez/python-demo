"""Configuration management for the translation service."""
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    
    # Application Configuration
    app_name: str = "Translation Service"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Logging Configuration
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Allowed languages for translation
ALLOWED_LANGUAGES = Literal["french", "spanish", "italian", "portuguese", "romanian"]

# Language mapping for OpenAI prompts
LANGUAGE_MAPPING = {
    "french": "French",
    "spanish": "Spanish",
    "italian": "Italian",
    "portuguese": "Portuguese",
    "romanian": "Romanian"
}


# Global settings instance
settings = Settings()

