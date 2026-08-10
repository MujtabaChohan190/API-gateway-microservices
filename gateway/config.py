from pathlib import Path
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # JWT Configuration
    SECRET_KEY: str
    ALGORITHM: str

    # Redis Configuration
    REDIS_HOST: str
    REDIS_PORT: int

    GATEWAY_TIMEOUT: float
    CACHE_TTL: int

    USER_SERVICE_URL: HttpUrl
    PRODUCTS_SERVICE_URL: HttpUrl
    AUTH_SERVICE_URL: HttpUrl

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env"
    )


settings = Settings()


# Service Registry
SERVICES = {
    "users": str(settings.USER_SERVICE_URL),
    "products": str(settings.PRODUCTS_SERVICE_URL),
    "auth": str(settings.AUTH_SERVICE_URL),
}