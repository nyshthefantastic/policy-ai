from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str


class VersionResponse(BaseModel):
    service: str
    version: str


class ConfigCheckResponse(BaseModel):
    app_env: str
    database_connected: bool
    redis_configured: bool
    embedding_model: str
    embedding_dimension: int
    chat_model: str
    default_tenant_id: str
    retrieval_top_k: int
    min_confidence_threshold: float


class RequestContextResponse(BaseModel):
    tenant_id: str
    user_id: str
    user_roles: list[str]