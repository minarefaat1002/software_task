from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    
    Attributes:
        DATABASE_URL (str): The connection URL for the database in the format:
            postgresql+asyncpg://user:password@host:port/database
    """
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",        # Load variables from .env file
        extra="ignore"          # Silently ignore extra environment variables
    )

Config = Settings()
