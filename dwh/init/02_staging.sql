-- =============================================================================
-- staging — raw landing tables (mirror of source extracts)
-- =============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_core_loans (
    stg_id              BIGSERIAL PRIMARY KEY,
    loan_id             VARCHAR(64),
    customer_id         VARCHAR(64),
    product_code        VARCHAR(32),
    principal_amount    NUMERIC(18, 2),
    outstanding_balance NUMERIC(18, 2),
    interest_rate       NUMERIC(8, 4),
    disbursement_date   DATE,
    maturity_date       DATE,
    days_past_due       INTEGER,
    status_code         VARCHAR(16),
    currency_code       VARCHAR(3),
    branch_code         VARCHAR(16),
    source_updated_at   TIMESTAMPTZ,
    _extracted_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    _batch_id           UUID NOT NULL,
    _source_system      VARCHAR(64) NOT NULL DEFAULT 'CORE_DB'
);

CREATE TABLE IF NOT EXISTS staging.stg_acc_journal (
    stg_id              BIGSERIAL PRIMARY KEY,
    journal_id          VARCHAR(64),
    account_code        VARCHAR(32),
    account_name        VARCHAR(256),
    debit_amount        NUMERIC(18, 2),
    credit_amount       NUMERIC(18, 2),
    posting_date        DATE,
    fiscal_period       VARCHAR(7),
    description         TEXT,
    source_updated_at   TIMESTAMPTZ,
    _extracted_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    _batch_id           UUID NOT NULL,
    _source_system      VARCHAR(64) NOT NULL DEFAULT 'ERP_ACC'
);

CREATE TABLE IF NOT EXISTS staging.stg_app_borrowers (
    stg_id              BIGSERIAL PRIMARY KEY,
    borrower_id         VARCHAR(64),
    register_no         VARCHAR(20),
    full_name           VARCHAR(256),
    phone               VARCHAR(32),
    income_monthly      NUMERIC(18, 2),
    employment_status   VARCHAR(32),
    credit_score        INTEGER,
    application_id      VARCHAR(64),
    application_status  VARCHAR(32),
    source_updated_at   TIMESTAMPTZ,
    _extracted_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    _batch_id           UUID NOT NULL,
    _source_system      VARCHAR(64) NOT NULL DEFAULT 'LOAN_APP'
);

CREATE TABLE IF NOT EXISTS staging.etl_batch_log (
    batch_id            UUID PRIMARY KEY,
    dag_run_id          VARCHAR(128),
    started_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at         TIMESTAMPTZ,
    status              VARCHAR(16) NOT NULL DEFAULT 'RUNNING',
    source_systems      TEXT[],
    rows_extracted      BIGINT DEFAULT 0,
    rows_loaded_core    BIGINT DEFAULT 0,
    rows_rejected       BIGINT DEFAULT 0,
    error_message       TEXT
);

CREATE INDEX IF NOT EXISTS idx_stg_loans_batch ON staging.stg_core_loans (_batch_id);
CREATE INDEX IF NOT EXISTS idx_stg_journal_batch ON staging.stg_acc_journal (_batch_id);
CREATE INDEX IF NOT EXISTS idx_stg_borrowers_batch ON staging.stg_app_borrowers (_batch_id);
