from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.config import get_settings
from app.db.session import check_database_connection
from app.models.schemas import (
    ConfigCheckResponse,
    HealthResponse,
    RequestContextResponse,
    VersionResponse,
)
from app.observability.logging import configure_logging
from app.observability.middleware import RequestLoggingMiddleware
from app.security.context import RequestContext, get_request_context


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )


@app.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    return VersionResponse(
        service=settings.app_name,
        version=settings.app_version,
    )


@app.get("/config-check", response_model=ConfigCheckResponse)
def config_check() -> ConfigCheckResponse:
    return ConfigCheckResponse(
        app_env=settings.app_env,
        database_connected=check_database_connection(),
        redis_configured=bool(settings.redis_url),
        embedding_model=settings.embedding_model,
        embedding_dimension=settings.embedding_dimension,
        chat_model=settings.chat_model,
        default_tenant_id=settings.default_tenant_id,
        retrieval_top_k=settings.retrieval_top_k,
        min_confidence_threshold=settings.min_confidence_threshold,
    )


@app.get("/me", response_model=RequestContextResponse)
def me(context: RequestContext = Depends(get_request_context)) -> RequestContextResponse:
    return RequestContextResponse(
        tenant_id=context.tenant_id,
        user_id=context.user_id,
        user_roles=context.user_roles,
    )