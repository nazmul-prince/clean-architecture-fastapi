import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Database
    database_url: str = os.environ.get("DB_URL")
    database_name: str = os.environ.get("DB_NAME")
    database_user: str = os.environ.get("DB_USERNAME")
    database_password: str = os.environ.get("DB_PASSWORD")
    database_schema: str = os.environ.get("DB_SCHEMA")
    pool_size: int = os.environ.get("POOL_SIZE")
    max_overflow: int = os.environ.get("MAX_OVERFLOW")
    pool_recycle: int = os.environ.get("POOL_RECYCLE")
    pool_timeout: int = os.environ.get("POOL_TIMEOUT")

    keycloak_base_url: str = os.environ.get("KEYCLOAK_BASE_URL")
    keycloak_realm: str = os.environ.get("KEYCLOAK_REALM")
    keycloak_token_url: str = os.environ.get("KEYCLOAK_TOKEN_URL")
    keycloak_authorization_url: str = os.environ.get("KEYCLOAK_AUTHORIZATION_URL")
    keycloak_introspect_url: str = os.environ.get("KEYCLOAK_INTROSPECT_URL")
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    grant_type: str = os.environ.get("GRANT_TYPE")
    subject_token_type: str = os.environ.get("SUBJECT_TOKEN_TYPE")
    subject_issuer: str = os.environ.get("SUBJECT_ISSUER")

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
            f"@{self.database_url}/{self.database_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
