-- =============================================================================
-- Seed data for local demo (SREP dashboards, lineage, dictionary, users)
-- Password for all demo users: ChangeMe123!  (bcrypt hash below)
-- =============================================================================

INSERT INTO app_auth.roles (role_code, role_name_mn, role_name_en) VALUES
    ('EXEC', 'Гүйцэтгэх захирал', 'Executive'),
    ('RISK', 'Эрсдэлийн шинжээч', 'Risk Analyst'),
    ('REPORT', 'Тайлангийн ажилтан', 'Reporting Officer'),
    ('AUDITOR', 'Аудитор', 'Auditor'),
    ('ADMIN', 'Системийн админ', 'Administrator')
ON CONFLICT (role_code) DO NOTHING;

-- bcrypt hash of ChangeMe123!
INSERT INTO app_auth.users (username, email, full_name, password_hash, role_id)
SELECT 'ceo', 'ceo@bbsb.local', 'Батбаяр Г.',
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oQ.Y5Y5Y5Y5Yu',
       r.role_id FROM app_auth.roles r WHERE r.role_code = 'EXEC'
ON CONFLICT (username) DO NOTHING;

INSERT INTO app_auth.users (username, email, full_name, password_hash, role_id)
SELECT 'risk', 'risk@bbsb.local', 'Сараа М.',
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oQ.Y5Y5Y5Y5Yu',
       r.role_id FROM app_auth.roles r WHERE r.role_code = 'RISK'
ON CONFLICT (username) DO NOTHING;

INSERT INTO app_auth.users (username, email, full_name, password_hash, role_id)
SELECT 'report', 'report@bbsb.local', 'Оюунчимэг Т.',
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oQ.Y5Y5Y5Y5Yu',
       r.role_id FROM app_auth.roles r WHERE r.role_code = 'REPORT'
ON CONFLICT (username) DO NOTHING;

INSERT INTO app_auth.users (username, email, full_name, password_hash, role_id)
SELECT 'auditor', 'auditor@bbsb.local', 'Эрдэнэ Б.',
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oQ.Y5Y5Y5Y5Yu',
       r.role_id FROM app_auth.roles r WHERE r.role_code = 'AUDITOR'
ON CONFLICT (username) DO NOTHING;

INSERT INTO app_auth.users (username, email, full_name, password_hash, role_id)
SELECT 'admin', 'admin@bbsb.local', 'Системийн Админ',
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G2oQ.Y5Y5Y5Y5Yu',
       r.role_id FROM app_auth.roles r WHERE r.role_code = 'ADMIN'
ON CONFLICT (username) DO NOTHING;

-- Fix: use a real bcrypt in app seed; SQL placeholder may not verify.
-- Backend will upsert correct hashes on startup.

-- Data Dictionary (sample — DAMA-DMBOK Data Governance)
INSERT INTO governance.data_dictionary
    (schema_name, table_name, column_name, business_name_mn, business_name_en,
     description_mn, description_en, data_type, unit_of_measure, is_pii, is_mandatory,
     data_owner, data_steward, classification)
VALUES
    ('dw_core', 'fact_loan', 'loan_id', 'Зээлийн дугаар', 'Loan ID',
     'Үндсэн банкны системийн зээлийн нэгдсэн түлхүүр', 'Core banking loan primary key',
     'VARCHAR(64)', NULL, FALSE, TRUE, 'Зээлийн хэлтэс', 'Data Steward — Credit', 'Internal'),
    ('dw_core', 'fact_loan', 'outstanding_balance', 'Үлдэгдэл дүн', 'Outstanding Balance',
     'Зээлийн одоогийн үндсэн үлдэгдэл', 'Current principal outstanding',
     'NUMERIC(18,2)', 'MNT', FALSE, TRUE, 'Зээлийн хэлтэс', 'Data Steward — Credit', 'Confidential'),
    ('dw_core', 'fact_loan', 'days_past_due', 'Хугацаа хэтрэлт (хоног)', 'Days Past Due',
     'Төлбөрийн хугацаа хэтэрсэн хоногийн тоо', 'Number of days past due',
     'INTEGER', 'days', FALSE, TRUE, 'Эрсдэлийн хэлтэс', 'Data Steward — Risk', 'Internal'),
    ('dw_core', 'fact_loan', 'npl_flag', 'Чанаргүй зээлийн тэмдэг', 'NPL Flag',
     'DPD >= 90 хоног бол чанаргүй зээл', 'True when DPD >= 90',
     'BOOLEAN', NULL, FALSE, TRUE, 'Эрсдэлийн хэлтэс', 'Data Steward — Risk', 'Internal'),
    ('dw_core', 'dim_customer', 'register_no', 'Регистрийн дугаар', 'National ID',
     'Харилцагчийн улсын бүртгэлийн дугаар', 'Customer national registration number',
     'VARCHAR(20)', NULL, TRUE, TRUE, 'Харилцагчийн үйлчилгээ', 'Data Steward — KYC', 'Restricted'),
    ('data_marts', 'mart_srep_credit_portfolio', 'npl_ratio_pct', 'NPL харьцаа', 'NPL Ratio %',
     'Чанаргүй зээлийн үлдэгдэл / Нийт зээлийн үлдэгдэл * 100', 'NPL balance / Total outstanding * 100',
     'NUMERIC(8,4)', '%', FALSE, TRUE, 'Эрсдэлийн хэлтэс', 'Data Steward — Risk', 'Confidential'),
    ('data_marts', 'mart_srep_capital_adequacy', 'car_pct', 'Капиталын хүрэлцээ', 'Capital Adequacy Ratio',
     'Нийт капитал / Эрсдэлээр жигнэсэн хөрөнгө * 100', 'Total capital / RWA * 100',
     'NUMERIC(8,4)', '%', FALSE, TRUE, 'Санхүүгийн хэлтэс', 'Data Steward — Finance', 'Confidential')
ON CONFLICT DO NOTHING;

-- Lineage graph: Source → Staging → Core → Mart → Report
INSERT INTO governance.lineage_nodes (node_id, node_type, display_name, schema_name, table_name, system_name, description) VALUES
    ('src_core_loans', 'source', 'Core Banking — Loans', NULL, 'LOANS', 'CORE_DB', 'Oracle/MSSQL loan master'),
    ('src_erp_journal', 'source', 'ERP — GL Journal', NULL, 'GL_JOURNAL', 'ERP_ACC', 'Accounting journal entries'),
    ('src_loan_app', 'source', 'Loan App — Borrowers', NULL, 'borrowers', 'LOAN_APP', 'REST API borrower profiles'),
    ('stg_core_loans', 'staging', 'stg_core_loans', 'staging', 'stg_core_loans', 'DWH', 'Raw loan extract'),
    ('stg_acc_journal', 'staging', 'stg_acc_journal', 'staging', 'stg_acc_journal', 'DWH', 'Raw journal extract'),
    ('stg_app_borrowers', 'staging', 'stg_app_borrowers', 'staging', 'stg_app_borrowers', 'DWH', 'Raw borrower extract'),
    ('core_fact_loan', 'core', 'fact_loan', 'dw_core', 'fact_loan', 'DWH', 'Cleaned loan facts + lineage'),
    ('core_dim_customer', 'core', 'dim_customer', 'dw_core', 'dim_customer', 'DWH', 'Customer dimension SCD'),
    ('core_fact_journal', 'core', 'fact_journal', 'dw_core', 'fact_journal', 'DWH', 'Cleaned journal facts'),
    ('mart_credit', 'mart', 'mart_srep_credit_portfolio', 'data_marts', 'mart_srep_credit_portfolio', 'DWH', 'SREP credit mart'),
    ('mart_capital', 'mart', 'mart_srep_capital_adequacy', 'data_marts', 'mart_srep_capital_adequacy', 'DWH', 'SREP capital mart'),
    ('mart_m1', 'mart', 'mart_reg_mongolbank_m1', 'data_marts', 'mart_reg_mongolbank_m1', 'DWH', 'Mongolbank M1'),
    ('rpt_srep_dash', 'report', 'SREP Executive Dashboard', NULL, NULL, 'PLATFORM', 'Frontend KPI dashboard'),
    ('rpt_m1_excel', 'report', 'Mongolbank M1 Excel Export', NULL, NULL, 'PLATFORM', 'Regulatory Excel/PDF')
ON CONFLICT (node_id) DO NOTHING;

INSERT INTO governance.lineage_edges (from_node_id, to_node_id, transform_type, transform_logic) VALUES
    ('src_core_loans', 'stg_core_loans', 'extract', 'Incremental SQL WHERE updated_at > last_watermark'),
    ('src_erp_journal', 'stg_acc_journal', 'extract', 'Monthly fiscal period pull via pyodbc'),
    ('src_loan_app', 'stg_app_borrowers', 'extract', 'REST GET /api/borrowers incremental'),
    ('stg_core_loans', 'core_fact_loan', 'clean', 'Null/type/range/uniqueness DQ + hash key'),
    ('stg_app_borrowers', 'core_dim_customer', 'clean', 'PII validate register_no + SCD Type 2'),
    ('stg_acc_journal', 'core_fact_journal', 'clean', 'Debit/credit balance check + hash'),
    ('core_fact_loan', 'mart_credit', 'aggregate', 'SUM/COUNT by as_of_date; NPL = DPD>=90'),
    ('core_fact_journal', 'mart_capital', 'aggregate', 'Tier1/Tier2 from GL accounts + RWA'),
    ('mart_credit', 'mart_m1', 'report_calc', 'Map NPL & portfolio to DPM M1 codes'),
    ('mart_credit', 'rpt_srep_dash', 'report_calc', 'API /api/srep/credit → Recharts'),
    ('mart_capital', 'rpt_srep_dash', 'report_calc', 'API /api/srep/capital → KPI cards'),
    ('mart_m1', 'rpt_m1_excel', 'report_calc', 'OpenPyXL template fill, no manual edit')
ON CONFLICT DO NOTHING;

-- Demo batch + core facts
DO $$
DECLARE
    v_batch UUID := 'a0000000-0000-4000-8000-000000000001';
    v_asof  DATE := CURRENT_DATE;
BEGIN
    INSERT INTO staging.etl_batch_log (batch_id, dag_run_id, status, source_systems, rows_extracted, rows_loaded_core, finished_at)
    VALUES (v_batch, 'seed_manual', 'SUCCESS', ARRAY['CORE_DB','ERP_ACC','LOAN_APP'], 8, 8, NOW())
    ON CONFLICT DO NOTHING;

    INSERT INTO dw_core.dim_customer
        (customer_id, register_no, full_name, phone, income_monthly, employment_status, credit_score,
         sys_source_system, sys_batch_id, sys_hash_key)
    VALUES
        ('C001', 'УБ90010101', 'Болд Дорж', '99112233', 2500000, 'EMPLOYED', 720, 'LOAN_APP', v_batch, md5('C001')),
        ('C002', 'УБ85050505', 'Сарнай Бат', '88112233', 1800000, 'SELF_EMP', 650, 'LOAN_APP', v_batch, md5('C002')),
        ('C003', 'УВ92020202', 'Төмөр Ган', '77112233', 3200000, 'EMPLOYED', 780, 'LOAN_APP', v_batch, md5('C003')),
        ('C004', 'ДД88080808', 'Номин Эрдэнэ', '95112233', 1500000, 'EMPLOYED', 580, 'LOAN_APP', v_batch, md5('C004'))
    ON CONFLICT DO NOTHING;

    INSERT INTO dw_core.fact_loan
        (loan_id, customer_id, product_code, principal_amount, outstanding_balance, interest_rate,
         disbursement_date, maturity_date, days_past_due, status_code, branch_code, as_of_date,
         sys_source_system, sys_batch_id, sys_hash_key)
    VALUES
        ('L1001', 'C001', 'CONS', 10000000, 7500000, 24.0, '2024-01-15', '2026-01-15', 0, 'ACTIVE', 'UB01', v_asof, 'CORE_DB', v_batch, md5('L1001')),
        ('L1002', 'C002', 'SME', 25000000, 22000000, 22.5, '2023-06-01', '2025-06-01', 45, 'WATCH', 'UB02', v_asof, 'CORE_DB', v_batch, md5('L1002')),
        ('L1003', 'C003', 'CONS', 5000000, 1200000, 26.0, '2024-03-10', '2025-03-10', 0, 'ACTIVE', 'UB01', v_asof, 'CORE_DB', v_batch, md5('L1003')),
        ('L1004', 'C004', 'SME', 40000000, 38000000, 21.0, '2022-11-20', '2025-11-20', 120, 'NPL', 'DN01', v_asof, 'CORE_DB', v_batch, md5('L1004')),
        ('L1005', 'C001', 'AUTO', 15000000, 9000000, 20.0, '2023-09-01', '2026-09-01', 15, 'ACTIVE', 'UB01', v_asof, 'CORE_DB', v_batch, md5('L1005')),
        ('L1006', 'C002', 'CONS', 3000000, 2800000, 28.0, '2024-08-01', '2025-08-01', 95, 'NPL', 'UB02', v_asof, 'CORE_DB', v_batch, md5('L1006'))
    ON CONFLICT DO NOTHING;

    INSERT INTO dw_core.fact_journal
        (journal_id, account_code, account_name, debit_amount, credit_amount, posting_date, fiscal_period,
         description, sys_source_system, sys_batch_id, sys_hash_key)
    VALUES
        ('J9001', '3010', 'Tier1 Capital', 0, 5000000000, v_asof, to_char(v_asof, 'YYYY-MM'), 'Equity', 'ERP_ACC', v_batch, md5('J9001')),
        ('J9002', '3020', 'Tier2 Capital', 0, 800000000, v_asof, to_char(v_asof, 'YYYY-MM'), 'Subordinated', 'ERP_ACC', v_batch, md5('J9002')),
        ('J9003', '1100', 'Cash & Liquid', 1200000000, 0, v_asof, to_char(v_asof, 'YYYY-MM'), 'Liquid assets', 'ERP_ACC', v_batch, md5('J9003'))
    ON CONFLICT DO NOTHING;

    INSERT INTO data_marts.mart_srep_credit_portfolio
        (as_of_date, total_loans, total_outstanding, performing_balance, watch_balance, npl_balance,
         npl_ratio_pct, avg_dpd, avg_interest_rate, sys_batch_id)
    VALUES (
        v_asof, 6, 80500000, 17700000, 22000000, 40800000,
        ROUND((40800000.0 / 80500000.0) * 100, 4), 45.83, 23.5833, v_batch
    ) ON CONFLICT (as_of_date) DO NOTHING;

    INSERT INTO data_marts.mart_srep_capital_adequacy
        (as_of_date, tier1_capital, tier2_capital, total_capital, risk_weighted_assets, car_pct, sys_batch_id)
    VALUES (v_asof, 5000000000, 800000000, 5800000000, 32000000000, 18.1250, v_batch)
    ON CONFLICT (as_of_date) DO NOTHING;

    INSERT INTO data_marts.mart_srep_liquidity
        (as_of_date, liquid_assets, short_term_liab, lcr_pct, sys_batch_id)
    VALUES (v_asof, 1200000000, 900000000, 133.3333, v_batch)
    ON CONFLICT (as_of_date) DO NOTHING;

    INSERT INTO data_marts.mart_reg_mongolbank_m1
        (reporting_period, dpm_code, dpm_label_mn, dpm_label_en, amount_mnt, formula_ref, source_mart, sys_batch_id)
    VALUES
        (to_char(v_asof, 'YYYY-MM'), 'M1.A.01', 'Нийт зээлийн үлдэгдэл', 'Total loan outstanding', 80500000, 'SUM(outstanding)', 'mart_srep_credit_portfolio', v_batch),
        (to_char(v_asof, 'YYYY-MM'), 'M1.A.02', 'Чанаргүй зээлийн үлдэгдэл', 'NPL outstanding', 40800000, 'SUM WHERE DPD>=90', 'mart_srep_credit_portfolio', v_batch),
        (to_char(v_asof, 'YYYY-MM'), 'M1.A.03', 'NPL харьцаа (%)', 'NPL ratio %', 50.6832, 'NPL/Total*100', 'mart_srep_credit_portfolio', v_batch),
        (to_char(v_asof, 'YYYY-MM'), 'M1.B.01', 'Капиталын хүрэлцээ (%)', 'CAR %', 18.1250, 'Capital/RWA*100', 'mart_srep_capital_adequacy', v_batch)
    ON CONFLICT DO NOTHING;

    INSERT INTO governance.dq_rule_results
        (batch_id, rule_code, rule_name, target_table, severity, passed, failed_rows, total_rows, details)
    VALUES
        (v_batch, 'NULL_LOAN_ID', 'Loan ID must not be null', 'stg_core_loans', 'CRITICAL', TRUE, 0, 6, '{"column":"loan_id"}'),
        (v_batch, 'RANGE_RATE', 'Interest rate must be >= 0', 'stg_core_loans', 'ERROR', TRUE, 0, 6, '{"column":"interest_rate"}'),
        (v_batch, 'UNIQ_LOAN', 'Loan ID uniqueness', 'stg_core_loans', 'ERROR', TRUE, 0, 6, '{"column":"loan_id"}'),
        (v_batch, 'RANGE_AMOUNT', 'Principal must be > 0', 'stg_core_loans', 'ERROR', TRUE, 0, 6, '{"column":"principal_amount"}')
    ON CONFLICT DO NOTHING;

    INSERT INTO governance.audit_trail (actor, action, entity_type, entity_id, after_state)
    VALUES ('system', 'SEED_LOAD', 'etl_batch', v_batch::text, '{"status":"SUCCESS","source":"06_seed.sql"}');
END $$;
