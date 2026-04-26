from fastapi import Header
from pydantic import BaseModel


class RequestContext(BaseModel):
    tenant_id: str
    user_id: str
    user_roles: list[str]


def parse_roles(raw_roles: str | None) -> list[str]:
    if not raw_roles:
        return ["engineering"]

    return [role.strip() for role in raw_roles.split(",") if role.strip()]


def get_request_context(
    x_tenant_id: str | None = Header(default="acme", alias="X-Tenant-ID"),
    x_user_id: str | None = Header(default="local-user", alias="X-User-ID"),
    x_user_roles: str | None = Header(default="engineering", alias="X-User-Roles"),
) -> RequestContext:
    return RequestContext(
        tenant_id=x_tenant_id or "acme",
        user_id=x_user_id or "local-user",
        user_roles=parse_roles(x_user_roles),
    )