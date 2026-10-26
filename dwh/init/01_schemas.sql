-- =============================================================================
-- DWH Schema Bootstrap — DAMA-DMBOK aligned layered architecture
-- staging → dw_core → data_marts (+ governance metadata)
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dw_core;
CREATE SCHEMA IF NOT EXISTS data_marts;
CREATE SCHEMA IF NOT EXISTS governance;
CREATE SCHEMA IF NOT EXISTS app_auth;

COMMENT ON SCHEMA staging IS 'Landing zone: raw extracts from source systems, no business transforms';
COMMENT ON SCHEMA dw_core IS 'Curated, cleaned, lineage-enriched enterprise core';
COMMENT ON SCHEMA data_marts IS 'Subject-oriented marts for SREP, regulatory reporting, dashboards';
COMMENT ON SCHEMA governance IS 'Data dictionary, lineage graph, DQ results, audit trail (DAMA-DMBOK)';
COMMENT ON SCHEMA app_auth IS 'Platform users, roles, RBAC for the reporting application';
