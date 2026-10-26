-- =============================================================================
-- EBA Data Point Model (DPM) meta-model — August 2013 database description
-- Adapted for ББСБ regulatory templates (e.g. Mongolbank M1)
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS dpm;
COMMENT ON SCHEMA dpm IS 'DPM metadata repository (framework, tables, dimensions, datapoints)';

CREATE TABLE IF NOT EXISTS dpm.reporting_framework (
    framework_id    SERIAL PRIMARY KEY,
    framework_code  VARCHAR(32) UNIQUE NOT NULL,
    framework_label VARCHAR(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS dpm.taxonomy (
    taxonomy_id     SERIAL PRIMARY KEY,
    framework_id    INTEGER NOT NULL REFERENCES dpm.reporting_framework(framework_id),
    taxonomy_code   VARCHAR(64) UNIQUE NOT NULL,
    taxonomy_label  VARCHAR(256) NOT NULL,
    from_date       DATE NOT NULL,
    to_date         DATE
);

CREATE TABLE IF NOT EXISTS dpm.module (
    module_id           SERIAL PRIMARY KEY,
    taxonomy_id         INTEGER NOT NULL REFERENCES dpm.taxonomy(taxonomy_id),
    module_code         VARCHAR(64) UNIQUE NOT NULL,
    module_label        VARCHAR(256) NOT NULL,
    default_frequency   VARCHAR(32) NOT NULL DEFAULT 'monthly'
);

CREATE TABLE IF NOT EXISTS dpm.table_def (
    table_id        SERIAL PRIMARY KEY,
    framework_id    INTEGER NOT NULL REFERENCES dpm.reporting_framework(framework_id),
    table_code      VARCHAR(64) NOT NULL,
    table_label     VARCHAR(256) NOT NULL,
    UNIQUE (framework_id, table_code)
);

CREATE TABLE IF NOT EXISTS dpm.table_group (
    table_group_id          SERIAL PRIMARY KEY,
    taxonomy_id             INTEGER NOT NULL REFERENCES dpm.taxonomy(taxonomy_id),
    table_group_code        VARCHAR(64) NOT NULL,
    table_group_label       VARCHAR(256) NOT NULL,
    parent_table_group_id   INTEGER REFERENCES dpm.table_group(table_group_id),
    ord                     INTEGER NOT NULL DEFAULT 1,
    level_no                INTEGER NOT NULL DEFAULT 1,
    path                    VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS dpm.table_version (
    table_vid       SERIAL PRIMARY KEY,
    table_id        INTEGER NOT NULL REFERENCES dpm.table_def(table_id),
    table_group_id  INTEGER REFERENCES dpm.table_group(table_group_id),
    table_code      VARCHAR(64) NOT NULL,
    from_date       DATE NOT NULL,
    to_date         DATE
);

CREATE TABLE IF NOT EXISTS dpm.module_table (
    module_id   INTEGER NOT NULL REFERENCES dpm.module(module_id),
    table_vid   INTEGER NOT NULL REFERENCES dpm.table_version(table_vid),
    ord         INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (module_id, table_vid)
);

CREATE TABLE IF NOT EXISTS dpm.axis (
    axis_id             SERIAL PRIMARY KEY,
    table_vid           INTEGER NOT NULL REFERENCES dpm.table_version(table_vid),
    axis_orientation    CHAR(1) NOT NULL CHECK (axis_orientation IN ('X','Y','Z')),
    axis_label          VARCHAR(128),
    axis_order          INTEGER NOT NULL DEFAULT 1,
    is_open_axis        BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS dpm.domain (
    domain_id               SERIAL PRIMARY KEY,
    domain_code             VARCHAR(64) UNIQUE NOT NULL,
    domain_label            VARCHAR(256) NOT NULL,
    is_typed_domain         BOOLEAN NOT NULL DEFAULT FALSE,
    domain_description      TEXT
);

CREATE TABLE IF NOT EXISTS dpm.dimension (
    dimension_id            SERIAL PRIMARY KEY,
    domain_id               INTEGER NOT NULL REFERENCES dpm.domain(domain_id),
    dimension_code          VARCHAR(64) UNIQUE NOT NULL,
    dimension_label         VARCHAR(256) NOT NULL,
    dimension_description   TEXT,
    is_typed                BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS dpm.member (
    member_id           SERIAL PRIMARY KEY,
    domain_id           INTEGER NOT NULL REFERENCES dpm.domain(domain_id),
    member_code         VARCHAR(64) NOT NULL,
    member_label        VARCHAR(256) NOT NULL,
    is_default_member   BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (domain_id, member_code)
);

CREATE TABLE IF NOT EXISTS dpm.metric (
    metric_id       INTEGER PRIMARY KEY REFERENCES dpm.member(member_id),
    data_type       VARCHAR(32) NOT NULL DEFAULT 'monetary',
    period_type     VARCHAR(16) NOT NULL DEFAULT 'instant' -- instant | duration
);

CREATE TABLE IF NOT EXISTS dpm.hierarchy (
    hierarchy_id            SERIAL PRIMARY KEY,
    domain_id               INTEGER NOT NULL REFERENCES dpm.domain(domain_id),
    hierarchy_code          VARCHAR(64) NOT NULL,
    hierarchy_label         VARCHAR(256) NOT NULL,
    hierarchy_description   TEXT
);

CREATE TABLE IF NOT EXISTS dpm.hierarchy_node (
    hierarchy_id        INTEGER NOT NULL REFERENCES dpm.hierarchy(hierarchy_id),
    member_id           INTEGER NOT NULL REFERENCES dpm.member(member_id),
    parent_member_id    INTEGER REFERENCES dpm.member(member_id),
    is_abstract         BOOLEAN NOT NULL DEFAULT FALSE,
    unary_operator      VARCHAR(8),
    ord                 INTEGER NOT NULL DEFAULT 1,
    level_no            INTEGER NOT NULL DEFAULT 1,
    path                VARCHAR(256),
    PRIMARY KEY (hierarchy_id, member_id)
);

CREATE TABLE IF NOT EXISTS dpm.axis_ordinate (
    ordinate_id             SERIAL PRIMARY KEY,
    axis_id                 INTEGER NOT NULL REFERENCES dpm.axis(axis_id),
    ordinate_code           VARCHAR(64) NOT NULL,
    ordinate_label          VARCHAR(256) NOT NULL,
    is_abstract_header      BOOLEAN NOT NULL DEFAULT FALSE,
    metric_id               INTEGER REFERENCES dpm.metric(metric_id),
    parent_ordinate_id      INTEGER REFERENCES dpm.axis_ordinate(ordinate_id),
    display_before_children BOOLEAN NOT NULL DEFAULT TRUE,
    ord                     INTEGER NOT NULL DEFAULT 1,
    level_no                INTEGER NOT NULL DEFAULT 1,
    path                    VARCHAR(256),
    categorisation_key      TEXT
);

CREATE TABLE IF NOT EXISTS dpm.ordinate_categorisation (
    ordinate_id     INTEGER NOT NULL REFERENCES dpm.axis_ordinate(ordinate_id),
    dimension_id    INTEGER NOT NULL REFERENCES dpm.dimension(dimension_id),
    member_id       INTEGER NOT NULL REFERENCES dpm.member(member_id),
    PRIMARY KEY (ordinate_id, dimension_id)
);

CREATE TABLE IF NOT EXISTS dpm.context_of_datapoints (
    context_id      SERIAL PRIMARY KEY,
    context_key     TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dpm.context_definition (
    context_id      INTEGER NOT NULL REFERENCES dpm.context_of_datapoints(context_id),
    dimension_id    INTEGER NOT NULL REFERENCES dpm.dimension(dimension_id),
    member_id       INTEGER NOT NULL REFERENCES dpm.member(member_id),
    PRIMARY KEY (context_id, dimension_id)
);

CREATE TABLE IF NOT EXISTS dpm.data_point (
    data_point_id           SERIAL PRIMARY KEY,
    related_data_point_id   INTEGER REFERENCES dpm.data_point(data_point_id)
);

CREATE TABLE IF NOT EXISTS dpm.data_point_version (
    data_point_vid      SERIAL PRIMARY KEY,
    data_point_id       INTEGER NOT NULL REFERENCES dpm.data_point(data_point_id),
    metric_id           INTEGER NOT NULL REFERENCES dpm.metric(metric_id),
    context_id          INTEGER NOT NULL REFERENCES dpm.context_of_datapoints(context_id),
    from_date           DATE NOT NULL,
    to_date             DATE,
    categorisation_key  TEXT NOT NULL,
    UNIQUE (categorisation_key, from_date)
);

CREATE TABLE IF NOT EXISTS dpm.table_cell (
    cell_id         SERIAL PRIMARY KEY,
    table_vid       INTEGER NOT NULL REFERENCES dpm.table_version(table_vid),
    data_point_id   INTEGER REFERENCES dpm.data_point(data_point_id),
    is_shaded       BOOLEAN NOT NULL DEFAULT FALSE,
    is_row_key      BOOLEAN NOT NULL DEFAULT FALSE,
    business_code   VARCHAR(64) -- e.g. M1.A.01 for UI convenience
);

CREATE TABLE IF NOT EXISTS dpm.cell_position (
    cell_id         INTEGER NOT NULL REFERENCES dpm.table_cell(cell_id),
    ordinate_id     INTEGER NOT NULL REFERENCES dpm.axis_ordinate(ordinate_id),
    PRIMARY KEY (cell_id, ordinate_id)
);

CREATE TABLE IF NOT EXISTS dpm.validation_rule (
    rule_id         SERIAL PRIMARY KEY,
    taxonomy_id     INTEGER REFERENCES dpm.taxonomy(taxonomy_id),
    rule_code       VARCHAR(64) NOT NULL,
    rule_label      VARCHAR(256) NOT NULL,
    expression      TEXT NOT NULL,
    severity        VARCHAR(16) NOT NULL DEFAULT 'ERROR'
);

CREATE TABLE IF NOT EXISTS dpm.fact_value (
    fact_id             BIGSERIAL PRIMARY KEY,
    data_point_id       INTEGER NOT NULL REFERENCES dpm.data_point(data_point_id),
    reporting_period    VARCHAR(7) NOT NULL,
    entity_code         VARCHAR(64) NOT NULL DEFAULT 'BBSB_HQ',
    amount              NUMERIC(18, 4) NOT NULL,
    currency_code       VARCHAR(3) DEFAULT 'MNT',
    sys_batch_id        UUID,
    sys_created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (data_point_id, reporting_period, entity_code)
);

COMMENT ON TABLE dpm.data_point IS 'Stable business fact identity across taxonomy versions (DPM Aug 2013)';
COMMENT ON TABLE dpm.data_point_version IS 'Categorisation of a DataPoint valid for a period; CategorisationKey unique';
COMMENT ON TABLE dpm.table_cell IS 'Intersection of axis ordinates; non-shaded cells map 1:1 to a DataPoint';
