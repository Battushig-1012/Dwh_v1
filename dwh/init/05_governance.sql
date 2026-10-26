-- =============================================================================
-- governance — DAMA-DMBOK: dictionary, lineage, DQ, audit trail
-- =============================================================================

CREATE TABLE IF NOT EXISTS governance.data_dictionary (
    dict_id             BIGSERIAL PRIMARY KEY,
    schema_name         VARCHAR(64) NOT NULL,
    table_name          VARCHAR(128) NOT NULL,
    column_name         VARCHAR(128) NOT NULL,
    business_name_mn    VARCHAR(256) NOT NULL,
    business_name_en    VARCHAR(256),
    description_mn      TEXT,
    description_en      TEXT,
    data_type           VARCHAR(64) NOT NULL,
    unit_of_measure     VARCHAR(32),
    is_pii              BOOLEAN NOT NULL DEFAULT FALSE,
    is_mandatory        BOOLEAN NOT NULL DEFAULT FALSE,
    data_owner          VARCHAR(128) NOT NULL,
    data_steward        VARCHAR(128),
    classification      VARCHAR(32) NOT NULL DEFAULT 'Internal',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (schema_name, table_name, column_name)
);

CREATE TABLE IF NOT EXISTS governance.lineage_nodes (
    node_id             VARCHAR(128) PRIMARY KEY,
    node_type           VARCHAR(32) NOT NULL, -- source | staging | core | mart | report
    display_name        VARCHAR(256) NOT NULL,
    schema_name         VARCHAR(64),
    table_name          VARCHAR(128),
    system_name         VARCHAR(64),
    description         TEXT
);

CREATE TABLE IF NOT EXISTS governance.lineage_edges (
    edge_id             BIGSERIAL PRIMARY KEY,
    from_node_id        VARCHAR(128) NOT NULL REFERENCES governance.lineage_nodes(node_id),
    to_node_id          VARCHAR(128) NOT NULL REFERENCES governance.lineage_nodes(node_id),
    transform_type      VARCHAR(64) NOT NULL, -- extract | clean | aggregate | report_calc
    transform_logic     TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (from_node_id, to_node_id, transform_type)
);

CREATE TABLE IF NOT EXISTS governance.dq_rule_results (
    result_id           BIGSERIAL PRIMARY KEY,
    batch_id            UUID NOT NULL,
    rule_code           VARCHAR(64) NOT NULL,
    rule_name           VARCHAR(256) NOT NULL,
    target_table        VARCHAR(128) NOT NULL,
    severity            VARCHAR(16) NOT NULL, -- INFO | WARN | ERROR | CRITICAL
    passed              BOOLEAN NOT NULL,
    failed_rows         BIGINT NOT NULL DEFAULT 0,
    total_rows          BIGINT NOT NULL DEFAULT 0,
    details             JSONB,
    checked_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS governance.audit_trail (
    audit_id            BIGSERIAL PRIMARY KEY,
    event_time          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actor               VARCHAR(128) NOT NULL,
    action              VARCHAR(64) NOT NULL,
    entity_type         VARCHAR(64) NOT NULL,
    entity_id           VARCHAR(128),
    before_state        JSONB,
    after_state         JSONB,
    ip_address          VARCHAR(64),
    correlation_id      UUID
);

CREATE INDEX IF NOT EXISTS idx_dq_batch ON governance.dq_rule_results (batch_id);
CREATE INDEX IF NOT EXISTS idx_audit_time ON governance.audit_trail (event_time DESC);
CREATE INDEX IF NOT EXISTS idx_dict_table ON governance.data_dictionary (schema_name, table_name);

-- Application auth / RBAC
CREATE TABLE IF NOT EXISTS app_auth.roles (
    role_id             SERIAL PRIMARY KEY,
    role_code           VARCHAR(32) UNIQUE NOT NULL,
    role_name_mn        VARCHAR(128) NOT NULL,
    role_name_en        VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS app_auth.users (
    user_id             SERIAL PRIMARY KEY,
    username            VARCHAR(64) UNIQUE NOT NULL,
    email               VARCHAR(256) UNIQUE NOT NULL,
    full_name           VARCHAR(256) NOT NULL,
    password_hash       VARCHAR(256) NOT NULL,
    role_id             INTEGER NOT NULL REFERENCES app_auth.roles(role_id),
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
