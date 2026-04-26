CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS tenants (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id),
    title TEXT NOT NULL,
    source_path TEXT NOT NULL,
    document_type TEXT NOT NULL,
    policy_domain TEXT,
    owner TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS document_versions (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    version TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    effective_date DATE,
    is_current BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    UNIQUE (document_id, version, content_hash)
);

CREATE TABLE IF NOT EXISTS chunks (
    id UUID PRIMARY KEY,
    tenant_id TEXT NOT NULL REFERENCES tenants(id),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    document_version_id UUID NOT NULL REFERENCES document_versions(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    section_heading TEXT,
    token_count INT,
    allowed_roles JSONB NOT NULL DEFAULT '[]',
    metadata JSONB NOT NULL DEFAULT '{}',
    embedding vector(1536),
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS documents_tenant_idx
ON documents (tenant_id);

CREATE INDEX IF NOT EXISTS documents_type_idx
ON documents (document_type);

CREATE INDEX IF NOT EXISTS documents_policy_domain_idx
ON documents (policy_domain);

CREATE INDEX IF NOT EXISTS document_versions_document_id_idx
ON document_versions (document_id);

CREATE INDEX IF NOT EXISTS document_versions_effective_date_idx
ON document_versions (effective_date);

CREATE INDEX IF NOT EXISTS chunks_tenant_idx
ON chunks (tenant_id);

CREATE INDEX IF NOT EXISTS chunks_document_id_idx
ON chunks (document_id);

CREATE INDEX IF NOT EXISTS chunks_document_version_id_idx
ON chunks (document_version_id);

CREATE INDEX IF NOT EXISTS chunks_allowed_roles_idx
ON chunks USING GIN (allowed_roles);

CREATE INDEX IF NOT EXISTS chunks_metadata_idx
ON chunks USING GIN (metadata);

CREATE INDEX IF NOT EXISTS chunks_content_fts_idx
ON chunks
USING GIN (to_tsvector('english', content));