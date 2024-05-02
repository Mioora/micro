from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str | None = None
    order_service_url: str | None = None
    for_test: bool | None = None
    delivery_login: str | None = None
    delivery_password: str | None = None
    keycloak_id: str | None = None
    keycloak_secret: str | None = None
    keycloak_url: str | None = None
    keycloak_realm: str | None = None

settings = Settings()

