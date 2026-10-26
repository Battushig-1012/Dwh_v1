-- =============================================================================
-- dw_core — cleaned, normalized entities with lineage meta-fields
-- =============================================================================

CREATE TABLE IF NOT EXISTS dw_core.dim_customer (
    customer_sk         BIGSERIAL PRIMARY KEY,
    customer_id         VARCHAR(64) NOT NULL,
    register_no         VARCHAR(20),
    full_name           VARCHAR(256) NOT NULL,
    phone               VARCHAR(32),
    income_monthly      NUMERIC(18, 2),
    employment_status   VARCHAR(32),
    credit_score        INTEGER,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    valid_from          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_to            TIMESTAMPTZ,
    -- Lineage / audit meta (BCBS 239)
    sys_source_system   VARCHAR(64) NOT NULL,
    sys_created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sys_updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sys_batch_id        UUID NOT NULL,
    sys_hash_key        VARCHAR(64) NOT NULL,
    UNIQUE (customer_id, valid_from)
);

CREATE TABLE IF NOT EXISTS dw_core.fact_loan (
    loan_sk             BIGSERIAL PRIMARY KEY,
    loan_id             VARCHAR(64) NOT NULL,
    customer_id         VARCHAR(64) NOT NULL,
    product_code        VARCHAR(32) NOT NULL,
    principal_amount    NUMERIC(18, 2) NOT NULL,
    outstanding_balance NUMERIC(18, 2) NOT NULL,
    interest_rate       NUMERIC(8, 4) NOT NULL,
    disbursement_date   DATE NOT NULL,
    maturity_date       DATE,
    days_past_due       INTEGER NOT NULL DEFAULT 0,
    status_code         VARCHAR(16) NOT NULL,
    currency_code       VARCHAR(3) NOT NULL DEFAULT 'MNT',
    branch_code         VARCHAR(16),
    npl_flag            BOOLEAN GENERATED ALWAYS AS (days_past_due >= 90) STORED,
    as_of_date          DATE NOT NULL,
    sys_source_system   VARCHAR(64) NOT NULL,
    sys_created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sys_updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sys_batch_id        UUID NOT NULL,
    sys_hash_key        VARCHAR(64) NOT NULL,
    UNIQUE (loan_id, as_of_date)
);

CREATE TABLE IF NOT EXISTS dw_core.fact_journal (
    journal_sk          BIGSERIAL PRIMARY KEY,
    journal_id          VARCHAR(64) NOT NULL,
    account_code        VARCHAR(32) NOT NULL,
    account_name        VARCHAR(256),
    debit_amount        NUMERIC(18, 2) NOT NULL DEFAULT 0,
    credit_amount       NUMERIC(18, 2) NOT NULL DEFAULT 0,
    posting_date        DATE NOT NULL,
    fiscal_period       VARCHAR(7) NOT NULL,
    description         TEXT,
    sys_source_system   VARCHAR(64) NOT NULL,
    sys_created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sys_updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sys_batch_id        UUID NOT NULL,
    sys_hash_key        VARCHAR(64) NOT NULL,
    UNIQUE (journal_id, posting_date)
);

CREATE INDEX IF NOT EXISTS idx_fact_loan_customer ON dw_core.fact_loan (customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_loan_dpd ON dw_core.fact_loan (days_past_due);
CREATE INDEX IF NOT EXISTS idx_fact_loan_asof ON dw_core.fact_loan (as_of_date);
CREATE INDEX IF NOT EXISTS idx_fact_journal_period ON dw_core.fact_journal (fiscal_period);
