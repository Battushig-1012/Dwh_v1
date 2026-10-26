"""In-memory MVP demo dataset — used when DEMO_MODE=true (no PostgreSQL required)."""

from __future__ import annotations

from datetime import date

AS_OF = date.today().isoformat()
PERIOD = date.today().strftime("%Y-%m")
BATCH = "a0000000-0000-4000-8000-000000000001"

# passlib bcrypt of ChangeMe123!
DEMO_PASSWORD_HASH = "$2b$12$uUwDsryV97jo/dfplT9aRuSs.24cxUIb3TfLWOaYmQuFPBYWK1EFG"

USERS = {
    "ceo": {"username": "ceo", "full_name": "Батбаяр Г.", "role_code": "EXEC", "password_hash": DEMO_PASSWORD_HASH, "is_active": True},
    "risk": {"username": "risk", "full_name": "Сараа М.", "role_code": "RISK", "password_hash": DEMO_PASSWORD_HASH, "is_active": True},
    "report": {"username": "report", "full_name": "Оюунчимэг Т.", "role_code": "REPORT", "password_hash": DEMO_PASSWORD_HASH, "is_active": True},
    "auditor": {"username": "auditor", "full_name": "Эрдэнэ Б.", "role_code": "AUDITOR", "password_hash": DEMO_PASSWORD_HASH, "is_active": True},
    "admin": {"username": "admin", "full_name": "Системийн Админ", "role_code": "ADMIN", "password_hash": DEMO_PASSWORD_HASH, "is_active": True},
}

CAPITAL = {
    "as_of_date": AS_OF,
    "tier1_capital": 5_000_000_000,
    "tier2_capital": 800_000_000,
    "total_capital": 5_800_000_000,
    "risk_weighted_assets": 32_000_000_000,
    "car_pct": 18.125,
    "regulatory_minimum": 12.0,
    "buffer_pct": 6.125,
}

CREDIT = {
    "as_of_date": AS_OF,
    "total_loans": 6,
    "total_outstanding": 80_500_000,
    "performing_balance": 17_700_000,
    "watch_balance": 22_000_000,
    "npl_balance": 40_800_000,
    "npl_ratio_pct": 50.6832,
    "avg_dpd": 45.83,
    "avg_interest_rate": 23.5833,
}

LIQUIDITY = {
    "as_of_date": AS_OF,
    "liquid_assets": 1_200_000_000,
    "short_term_liab": 900_000_000,
    "lcr_pct": 133.3333,
    "regulatory_minimum": 100.0,
}

LOANS = [
    {"loan_id": "L1001", "customer_id": "C001", "product_code": "CONS", "outstanding_balance": 7_500_000, "interest_rate": 24.0, "days_past_due": 0, "status_code": "ACTIVE", "npl_flag": False, "as_of_date": AS_OF, "sys_source_system": "CORE_DB", "sys_batch_id": BATCH},
    {"loan_id": "L1002", "customer_id": "C002", "product_code": "SME", "outstanding_balance": 22_000_000, "interest_rate": 22.5, "days_past_due": 45, "status_code": "WATCH", "npl_flag": False, "as_of_date": AS_OF, "sys_source_system": "CORE_DB", "sys_batch_id": BATCH},
    {"loan_id": "L1003", "customer_id": "C003", "product_code": "CONS", "outstanding_balance": 1_200_000, "interest_rate": 26.0, "days_past_due": 0, "status_code": "ACTIVE", "npl_flag": False, "as_of_date": AS_OF, "sys_source_system": "CORE_DB", "sys_batch_id": BATCH},
    {"loan_id": "L1004", "customer_id": "C004", "product_code": "SME", "outstanding_balance": 38_000_000, "interest_rate": 21.0, "days_past_due": 120, "status_code": "NPL", "npl_flag": True, "as_of_date": AS_OF, "sys_source_system": "CORE_DB", "sys_batch_id": BATCH},
    {"loan_id": "L1005", "customer_id": "C001", "product_code": "AUTO", "outstanding_balance": 9_000_000, "interest_rate": 20.0, "days_past_due": 15, "status_code": "ACTIVE", "npl_flag": False, "as_of_date": AS_OF, "sys_source_system": "CORE_DB", "sys_batch_id": BATCH},
    {"loan_id": "L1006", "customer_id": "C002", "product_code": "CONS", "outstanding_balance": 2_800_000, "interest_rate": 28.0, "days_past_due": 95, "status_code": "NPL", "npl_flag": True, "as_of_date": AS_OF, "sys_source_system": "CORE_DB", "sys_batch_id": BATCH},
]

M1 = [
    {"reporting_period": PERIOD, "dpm_code": "M1.A.01", "dpm_label_mn": "Нийт зээлийн үлдэгдэл", "dpm_label_en": "Total loan outstanding", "amount_mnt": 80_500_000, "formula_ref": "SUM(outstanding)", "source_mart": "mart_srep_credit_portfolio"},
    {"reporting_period": PERIOD, "dpm_code": "M1.A.02", "dpm_label_mn": "Чанаргүй зээлийн үлдэгдэл", "dpm_label_en": "NPL outstanding", "amount_mnt": 40_800_000, "formula_ref": "SUM WHERE DPD>=90", "source_mart": "mart_srep_credit_portfolio"},
    {"reporting_period": PERIOD, "dpm_code": "M1.A.03", "dpm_label_mn": "NPL харьцаа (%)", "dpm_label_en": "NPL ratio %", "amount_mnt": 50.6832, "formula_ref": "NPL/Total*100", "source_mart": "mart_srep_credit_portfolio"},
    {"reporting_period": PERIOD, "dpm_code": "M1.B.01", "dpm_label_mn": "Капиталын хүрэлцээ (%)", "dpm_label_en": "CAR %", "amount_mnt": 18.125, "formula_ref": "Capital/RWA*100", "source_mart": "mart_srep_capital_adequacy"},
]

LINEAGE_NODES = [
    {"id": "src_core_loans", "type": "source", "label": "Core Banking — Loans", "schema_name": None, "table_name": "LOANS", "system_name": "CORE_DB", "description": "Oracle/MSSQL loan master"},
    {"id": "src_erp_journal", "type": "source", "label": "ERP — GL Journal", "schema_name": None, "table_name": "GL_JOURNAL", "system_name": "ERP_ACC", "description": "Accounting journal entries"},
    {"id": "src_loan_app", "type": "source", "label": "Loan App — Borrowers", "schema_name": None, "table_name": "borrowers", "system_name": "LOAN_APP", "description": "REST API borrower profiles"},
    {"id": "stg_core_loans", "type": "staging", "label": "stg_core_loans", "schema_name": "staging", "table_name": "stg_core_loans", "system_name": "DWH", "description": "Raw loan extract"},
    {"id": "stg_acc_journal", "type": "staging", "label": "stg_acc_journal", "schema_name": "staging", "table_name": "stg_acc_journal", "system_name": "DWH", "description": "Raw journal extract"},
    {"id": "stg_app_borrowers", "type": "staging", "label": "stg_app_borrowers", "schema_name": "staging", "table_name": "stg_app_borrowers", "system_name": "DWH", "description": "Raw borrower extract"},
    {"id": "core_fact_loan", "type": "core", "label": "fact_loan", "schema_name": "dw_core", "table_name": "fact_loan", "system_name": "DWH", "description": "Cleaned loan facts + lineage"},
    {"id": "core_dim_customer", "type": "core", "label": "dim_customer", "schema_name": "dw_core", "table_name": "dim_customer", "system_name": "DWH", "description": "Customer dimension SCD"},
    {"id": "core_fact_journal", "type": "core", "label": "fact_journal", "schema_name": "dw_core", "table_name": "fact_journal", "system_name": "DWH", "description": "Cleaned journal facts"},
    {"id": "mart_credit", "type": "mart", "label": "mart_srep_credit_portfolio", "schema_name": "data_marts", "table_name": "mart_srep_credit_portfolio", "system_name": "DWH", "description": "SREP credit mart"},
    {"id": "mart_capital", "type": "mart", "label": "mart_srep_capital_adequacy", "schema_name": "data_marts", "table_name": "mart_srep_capital_adequacy", "system_name": "DWH", "description": "SREP capital mart"},
    {"id": "mart_m1", "type": "mart", "label": "mart_reg_mongolbank_m1", "schema_name": "data_marts", "table_name": "mart_reg_mongolbank_m1", "system_name": "DWH", "description": "Mongolbank M1"},
    {"id": "rpt_srep_dash", "type": "report", "label": "SREP Executive Dashboard", "schema_name": None, "table_name": None, "system_name": "PLATFORM", "description": "Frontend KPI dashboard"},
    {"id": "rpt_m1_excel", "type": "report", "label": "Mongolbank M1 Excel Export", "schema_name": None, "table_name": None, "system_name": "PLATFORM", "description": "Regulatory Excel/PDF"},
]

LINEAGE_EDGES = [
    {"edge_id": 1, "source": "src_core_loans", "target": "stg_core_loans", "transform_type": "extract", "transform_logic": "Incremental SQL WHERE updated_at > last_watermark"},
    {"edge_id": 2, "source": "src_erp_journal", "target": "stg_acc_journal", "transform_type": "extract", "transform_logic": "Monthly fiscal period pull"},
    {"edge_id": 3, "source": "src_loan_app", "target": "stg_app_borrowers", "transform_type": "extract", "transform_logic": "REST GET /api/borrowers"},
    {"edge_id": 4, "source": "stg_core_loans", "target": "core_fact_loan", "transform_type": "clean", "transform_logic": "Null/type/range/uniqueness DQ + hash key"},
    {"edge_id": 5, "source": "stg_app_borrowers", "target": "core_dim_customer", "transform_type": "clean", "transform_logic": "PII validate + SCD Type 2"},
    {"edge_id": 6, "source": "stg_acc_journal", "target": "core_fact_journal", "transform_type": "clean", "transform_logic": "Debit/credit balance check"},
    {"edge_id": 7, "source": "core_fact_loan", "target": "mart_credit", "transform_type": "aggregate", "transform_logic": "SUM/COUNT; NPL = DPD>=90"},
    {"edge_id": 8, "source": "core_fact_journal", "target": "mart_capital", "transform_type": "aggregate", "transform_logic": "Tier1/Tier2 + RWA"},
    {"edge_id": 9, "source": "mart_credit", "target": "mart_m1", "transform_type": "report_calc", "transform_logic": "Map to DPM M1 codes"},
    {"edge_id": 10, "source": "mart_credit", "target": "rpt_srep_dash", "transform_type": "report_calc", "transform_logic": "API → Recharts"},
    {"edge_id": 11, "source": "mart_capital", "target": "rpt_srep_dash", "transform_type": "report_calc", "transform_logic": "API → KPI cards"},
    {"edge_id": 12, "source": "mart_m1", "target": "rpt_m1_excel", "transform_type": "report_calc", "transform_logic": "OpenPyXL export"},
]

DICTIONARY = [
    {"dict_id": 1, "schema_name": "dw_core", "table_name": "fact_loan", "column_name": "loan_id", "business_name_mn": "Зээлийн дугаар", "business_name_en": "Loan ID", "description_mn": "Үндсэн банкны системийн зээлийн нэгдсэн түлхүүр", "description_en": "Core banking loan key", "data_type": "VARCHAR(64)", "unit_of_measure": None, "is_pii": False, "is_mandatory": True, "data_owner": "Зээлийн хэлтэс", "data_steward": "Data Steward — Credit", "classification": "Internal"},
    {"dict_id": 2, "schema_name": "dw_core", "table_name": "fact_loan", "column_name": "outstanding_balance", "business_name_mn": "Үлдэгдэл дүн", "business_name_en": "Outstanding Balance", "description_mn": "Зээлийн одоогийн үндсэн үлдэгдэл", "description_en": "Current principal", "data_type": "NUMERIC(18,2)", "unit_of_measure": "MNT", "is_pii": False, "is_mandatory": True, "data_owner": "Зээлийн хэлтэс", "data_steward": "Data Steward — Credit", "classification": "Confidential"},
    {"dict_id": 3, "schema_name": "dw_core", "table_name": "fact_loan", "column_name": "days_past_due", "business_name_mn": "Хугацаа хэтрэлт (хоног)", "business_name_en": "Days Past Due", "description_mn": "Төлбөрийн хугацаа хэтэрсэн хоног", "description_en": "Days past due", "data_type": "INTEGER", "unit_of_measure": "days", "is_pii": False, "is_mandatory": True, "data_owner": "Эрсдэлийн хэлтэс", "data_steward": "Data Steward — Risk", "classification": "Internal"},
    {"dict_id": 4, "schema_name": "data_marts", "table_name": "mart_srep_credit_portfolio", "column_name": "npl_ratio_pct", "business_name_mn": "NPL харьцаа", "business_name_en": "NPL Ratio %", "description_mn": "Чанаргүй зээл / Нийт үлдэгдэл * 100", "description_en": "NPL / Total * 100", "data_type": "NUMERIC(8,4)", "unit_of_measure": "%", "is_pii": False, "is_mandatory": True, "data_owner": "Эрсдэлийн хэлтэс", "data_steward": "Data Steward — Risk", "classification": "Confidential"},
    {"dict_id": 5, "schema_name": "data_marts", "table_name": "mart_srep_capital_adequacy", "column_name": "car_pct", "business_name_mn": "Капиталын хүрэлцээ", "business_name_en": "CAR", "description_mn": "Нийт капитал / RWA * 100", "description_en": "Capital / RWA * 100", "data_type": "NUMERIC(8,4)", "unit_of_measure": "%", "is_pii": False, "is_mandatory": True, "data_owner": "Санхүүгийн хэлтэс", "data_steward": "Data Steward — Finance", "classification": "Confidential"},
]

BATCHES = [
    {
        "batch_id": BATCH,
        "dag_run_id": "demo_seed",
        "started_at": f"{AS_OF}T02:00:00+08:00",
        "finished_at": f"{AS_OF}T02:12:00+08:00",
        "status": "SUCCESS",
        "source_systems": ["CORE_DB", "ERP_ACC", "LOAN_APP"],
        "rows_extracted": 8,
        "rows_loaded_core": 8,
        "rows_rejected": 0,
        "error_message": None,
    }
]

DQ_RESULTS = [
    {"result_id": 1, "batch_id": BATCH, "rule_code": "NULL_LOAN_ID", "rule_name": "Loan ID must not be null", "target_table": "stg_core_loans", "severity": "CRITICAL", "passed": True, "failed_rows": 0, "total_rows": 6, "details": {"column": "loan_id"}, "checked_at": f"{AS_OF}T02:05:00+08:00"},
    {"result_id": 2, "batch_id": BATCH, "rule_code": "RANGE_RATE", "rule_name": "Interest rate must be >= 0", "target_table": "stg_core_loans", "severity": "ERROR", "passed": True, "failed_rows": 0, "total_rows": 6, "details": {"column": "interest_rate"}, "checked_at": f"{AS_OF}T02:05:00+08:00"},
    {"result_id": 3, "batch_id": BATCH, "rule_code": "UNIQ_LOAN", "rule_name": "Loan ID uniqueness", "target_table": "stg_core_loans", "severity": "ERROR", "passed": True, "failed_rows": 0, "total_rows": 6, "details": {"column": "loan_id"}, "checked_at": f"{AS_OF}T02:05:00+08:00"},
]

AUDIT = [
    {"audit_id": 1, "event_time": f"{AS_OF}T02:12:00+08:00", "actor": "system", "action": "SEED_LOAD", "entity_type": "etl_batch", "entity_id": BATCH, "after_state": {"status": "SUCCESS", "mode": "demo"}},
]


def srep_overview() -> dict:
    return {
        "capital": CAPITAL,
        "credit": CREDIT,
        "liquidity": LIQUIDITY,
        "pillars": [
            {"code": "CAPITAL", "name_mn": "Капитал", "value": CAPITAL["car_pct"], "unit": "%", "threshold": 12.0},
            {"code": "LIQUIDITY", "name_mn": "Хөрвөх чадвар", "value": LIQUIDITY["lcr_pct"], "unit": "%", "threshold": 100.0},
            {"code": "CREDIT", "name_mn": "Зээлийн чанар", "value": CREDIT["avg_dpd"], "unit": "DPD", "threshold": 30.0},
            {"code": "NPL", "name_mn": "NPL харьцаа", "value": CREDIT["npl_ratio_pct"], "unit": "%", "threshold": 5.0},
        ],
        "demo_mode": True,
    }
