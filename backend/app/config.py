from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="PolicyOps AI", alias="APP_NAME")
    app_env: str = Field(default="local", alias="APP_ENV")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")

    database_url: str = Field(
        default="postgresql+psycopg://policyops:policyops@localhost:5432/policyops",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    chat_model: str = Field(default="gpt-4.1-mini", alias="CHAT_MODEL")
    embedding_model: str = Field(default="text-embedding-3-small", alias="EMBEDDING_MODEL")
    embedding_dimension: int = Field(default=1536, alias="EMBEDDING_DIMENSION")

    default_tenant_id: str = Field(default="acme", alias="DEFAULT_TENANT_ID")
    default_rate_limit_per_minute: int = Field(default=20, alias="DEFAULT_RATE_LIMIT_PER_MINUTE")

    min_confidence_threshold: float = Field(default=0.55, alias="MIN_CONFIDENCE_THRESHOLD")
    retrieval_top_k: int = Field(default=8, alias="RETRIEVAL_TOP_K")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()