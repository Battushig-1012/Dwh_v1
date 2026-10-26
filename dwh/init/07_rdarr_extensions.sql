-- Optional RDARR extensions for live PostgreSQL (DEMO_MODE=false future path)
-- Aligns with ECB SSM Guide May 2024 §§3.2–3.7

CREATE TABLE IF NOT EXISTS governance.rdarr_scope_report (
    report_id       VARCHAR(64) PRIMARY KEY,
    category        VARCHAR(32) NOT NULL,
    name            VARCHAR(256) NOT NULL,
    frequency       VARCHAR(32) NOT NULL,
    owner_role      VARCHAR(64),
    in_scope        BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS governance.rdarr_cde (
    cde_id          VARCHAR(64) PRIMARY KEY,
    schema_name     VARCHAR(64) NOT NULL,
    table_name      VARCHAR(128) NOT NULL,
    column_name     VARCHAR(128) NOT NULL,
    data_owner      VARCHAR(128) NOT NULL,
    validation_rule TEXT,
    kri_links       TEXT[]
);

CREATE TABLE IF NOT EXISTS governance.dq_kpi (
    kpi_code        VARCHAR(64) PRIMARY KEY,
    dimension       VARCHAR(32) NOT NULL,
    name_mn         VARCHAR(256) NOT NULL,
    value_num       NUMERIC(18,4),
    tolerance_num   NUMERIC(18,4),
    unit            VARCHAR(32),
    status          VARCHAR(16),
    as_of_date      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS governance.dq_issue_register (
    issue_id            VARCHAR(64) PRIMARY KEY,
    title               TEXT NOT NULL,
    severity            VARCHAR(16) NOT NULL,
    status              VARCHAR(16) NOT NULL,
    dimension           VARCHAR(32),
    affected_kri        VARCHAR(64),
    root_cause          TEXT,
    impact_analysis     TEXT,
    owner_role          VARCHAR(64),
    opened_at           DATE,
    due_at              DATE,
    remediation_plan    TEXT
);

CREATE TABLE IF NOT EXISTS governance.manual_workaround (
    workaround_id       VARCHAR(64) PRIMARY KEY,
    name                VARCHAR(256) NOT NULL,
    workaround_type     VARCHAR(64),
    in_scope            BOOLEAN DEFAULT TRUE,
    controls            TEXT[],
    owner_role          VARCHAR(64),
    status              VARCHAR(32),
    target_automation   TEXT
);

CREATE TABLE IF NOT EXISTS governance.reporting_sla (
    report_id           VARCHAR(64) PRIMARY KEY,
    frequency           VARCHAR(32),
    sla_working_days    INTEGER,
    cutoff_label        VARCHAR(64),
    last_produced_at    TIMESTAMPTZ,
    production_days     NUMERIC(8,2),
    within_sla          BOOLEAN
);

CREATE TABLE IF NOT EXISTS governance.implementation_milestone (
    milestone_id        VARCHAR(32) PRIMARY KEY,
    title               TEXT NOT NULL,
    due_date            DATE,
    status              VARCHAR(32),
    progress_pct        INTEGER DEFAULT 0
);

COMMENT ON TABLE governance.dq_issue_register IS 'SSM 3.5 data quality issue register';
COMMENT ON TABLE governance.rdarr_cde IS 'SSM 3.2/3.4 critical data elements';
