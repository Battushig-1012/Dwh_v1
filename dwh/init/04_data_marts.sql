-- =============================================================================
-- data_marts — SREP / Mongolbank / FRC ready aggregates
-- =============================================================================

CREATE TABLE IF NOT EXISTS data_marts.mart_srep_capital_adequacy (
    mart_id             BIGSERIAL PRIMARY KEY,
    as_of_date          DATE NOT NULL,
    tier1_capital       NUMERIC(18, 2) NOT NULL,
    tier2_capital       NUMERIC(18, 2) NOT NULL,
    total_capital       NUMERIC(18, 2) NOT NULL,
    risk_weighted_assets NUMERIC(18, 2) NOT NULL,
    car_pct             NUMERIC(8, 4) NOT NULL,
    regulatory_minimum  NUMERIC(8, 4) NOT NULL DEFAULT 12.0,
    buffer_pct          NUMERIC(8, 4) GENERATED ALWAYS AS (car_pct - regulatory_minimum) STORED,
    sys_batch_id        UUID NOT NULL,
    sys_created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (as_of_date)
);

CREATE TABLE IF NOT EXISTS data_marts.mart_srep_credit_portfolio (
    mart_id             BIGSERIAL PRIMARY KEY,
    as_of_date          DATE NOT NULL,
    total_loans         INTEGER NOT NULL,
    total_outstanding   NUMERIC(18, 2) NOT NULL,
    performing_balance  NUMERIC(18, 2) NOT NULL,
    watch_balance       NUMERIC(18, 2) NOT NULL,
    npl_balance         NUMERIC(18, 2) NOT NULL,
    npl_ratio_pct       NUMERIC(8, 4) NOT NULL,
    avg_dpd             NUMERIC(10, 2) NOT NULL,
    avg_interest_rate   NUMERIC(8, 4) NOT NULL,
    sys_batch_id        UUID NOT NULL,
    sys_created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (as_of_date)
);

CREATE TABLE IF NOT EXISTS data_marts.mart_reg_mongolbank_m1 (
    mart_id             BIGSERIAL PRIMARY KEY,
    reporting_period    VARCHAR(7) NOT NULL,
    dpm_code            VARCHAR(32) NOT NULL,
    dpm_label_mn        VARCHAR(256) NOT NULL,
    dpm_label_en        VARCHAR(256),
    amount_mnt          NUMERIC(18, 2) NOT NULL,
    formula_ref         VARCHAR(128),
    source_mart         VARCHAR(128),
    sys_batch_id        UUID NOT NULL,
    sys_created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (reporting_period, dpm_code)
);

CREATE TABLE IF NOT EXISTS data_marts.mart_srep_liquidity (
    mart_id             BIGSERIAL PRIMARY KEY,
    as_of_date          DATE NOT NULL,
    liquid_assets       NUMERIC(18, 2) NOT NULL,
    short_term_liab     NUMERIC(18, 2) NOT NULL,
    lcr_pct             NUMERIC(8, 4) NOT NULL,
    regulatory_minimum  NUMERIC(8, 4) NOT NULL DEFAULT 100.0,
    sys_batch_id        UUID NOT NULL,
    sys_created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (as_of_date)
);

COMMENT ON TABLE data_marts.mart_srep_capital_adequacy IS 'SREP pillar: Capital Adequacy';
COMMENT ON TABLE data_marts.mart_srep_credit_portfolio IS 'SREP pillar: Credit quality / NPL';
COMMENT ON TABLE data_marts.mart_reg_mongolbank_m1 IS 'Mongolbank M1 regulatory template (DPM coded)';
COMMENT ON TABLE data_marts.mart_srep_liquidity IS 'SREP pillar: Liquidity';
