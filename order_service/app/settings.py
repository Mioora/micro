
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_url: str | None = None
    amqp_url: str | None = None
    amqp_port: str | None = None
    for_test: bool | None = None
    keycloak_url: str | None = None
    keycloak_realm: str | None = None
    keycloak_secret: str | None = None
    keycloak_id: str | None = None

settings = Settings()