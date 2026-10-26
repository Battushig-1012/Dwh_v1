"""
ECB SSM Guide on effective RDARR (May 2024) — demo dataset.
Maps Sections 3.1–3.7 into platform-ready structures for ББСБ MVP.
"""

from __future__ import annotations

from datetime import date, timedelta

TODAY = date.today()
AS_OF = TODAY.isoformat()

# ---------------------------------------------------------------------------
# 3.1 Management body accountability
# ---------------------------------------------------------------------------
MANAGEMENT_BODY = {
    "accountable_body": "Гүйцэтгэх захирлын зөвлөл / Эрсдэлийн хороо",
    "rdarr_sponsors": [
        {"role": "CRO", "name": "Сараа М.", "username": "risk", "responsibility": "Data governance framework implementation"},
        {"role": "CFO", "name": "Оюунчимэг Т.", "username": "report", "responsibility": "Financial & supervisory reporting integrity"},
    ],
    "priorities": [
        "RDARR нь эрсдэлийн засаглалын гол тэргүүлэх чиглэл",
        "DQ KPI-г улирал бүр удирдлагын зөвлөлд тайлагнах",
        "BCBS 239 adherence self-assessment жил бүр шинэчлэх",
    ],
    "last_training": (TODAY - timedelta(days=45)).isoformat(),
    "collective_suitability_note": "Удирдлагын гишүүдэд дата/IT/эрсдэлийн сургалт төлөвлөгдсөн (SSM 3.1.9–11)",
}

# ---------------------------------------------------------------------------
# 3.2 Scope of application — reports, models, KRIs, critical data elements
# ---------------------------------------------------------------------------
SCOPE = {
    "legal_entities": [
        {"code": "BBSB_HQ", "name_mn": "ББСБ төв", "material": True, "in_scope": True},
        {"code": "BBSB_BR_UB", "name_mn": "Улаанбаатар салбар", "material": True, "in_scope": True},
    ],
    "risk_types": [
        {"code": "CREDIT", "name_mn": "Зээлийн эрсдэл", "in_scope": True},
        {"code": "LIQUIDITY", "name_mn": "Хөрвөх чадварын эрсдэл", "in_scope": True},
        {"code": "CAPITAL", "name_mn": "Капиталын хүрэлцээ", "in_scope": True},
        {"code": "OPERATIONAL", "name_mn": "Үйл ажиллагааны эрсдэл", "in_scope": True},
        {"code": "CLIMATE", "name_mn": "Уур амьсгал / байгаль орчин", "in_scope": False, "note": "Phase-2 roadmap"},
    ],
    "reports": [
        {"id": "RPT_SREP_EXEC", "category": "internal_risk", "name": "SREP Executive Dashboard", "frequency": "daily", "owner": "RISK", "in_scope": True},
        {"id": "RPT_CREDIT_PORT", "category": "internal_risk", "name": "Credit Portfolio & NPL", "frequency": "daily", "owner": "RISK", "in_scope": True},
        {"id": "RPT_LIQ", "category": "internal_risk", "name": "Liquidity / LCR", "frequency": "daily", "owner": "RISK", "in_scope": True},
        {"id": "RPT_M1", "category": "supervisory", "name": "Монголбанк M1", "frequency": "monthly", "owner": "REPORT", "in_scope": True},
        {"id": "RPT_SZH", "category": "supervisory", "name": "СЗХ тайлан", "frequency": "monthly", "owner": "REPORT", "in_scope": True},
        {"id": "RPT_FIN_STMT", "category": "financial", "name": "Санхүүгийн тайлан (жил)", "frequency": "annual", "owner": "CFO", "in_scope": True},
    ],
    "models": [
        {"id": "MDL_NPL", "name": "NPL classification (DPD>=90)", "pillar": "P2", "owner": "RISK", "in_scope": True},
        {"id": "MDL_CAR", "name": "Capital Adequacy Ratio", "pillar": "P1/P2", "owner": "FINANCE", "in_scope": True},
        {"id": "MDL_LCR", "name": "Liquidity Coverage Ratio (simplified)", "pillar": "P2", "owner": "TREASURY", "in_scope": True},
        {"id": "MDL_IFRS9", "name": "IFRS9 ECL (collective)", "pillar": "accounting", "owner": "FINANCE", "in_scope": False, "note": "Planned Q3"},
    ],
    "kris": [
        {"kri_id": "KRI_CAR", "name_mn": "Капиталын хүрэлцээ (CAR)", "unit": "%", "limit": 12.0, "appetite": 14.0, "current": 18.125, "direction": "higher_better", "cde_ids": ["CDE_TIER1", "CDE_TIER2", "CDE_RWA"]},
        {"kri_id": "KRI_NPL", "name_mn": "NPL харьцаа", "unit": "%", "limit": 5.0, "appetite": 3.0, "current": 50.6832, "direction": "lower_better", "cde_ids": ["CDE_OUTSTANDING", "CDE_DPD", "CDE_NPL_FLAG"]},
        {"kri_id": "KRI_LCR", "name_mn": "LCR", "unit": "%", "limit": 100.0, "appetite": 110.0, "current": 133.3333, "direction": "higher_better", "cde_ids": ["CDE_LIQUID", "CDE_ST_LIAB"]},
        {"kri_id": "KRI_DPD_AVG", "name_mn": "Дундаж DPD", "unit": "days", "limit": 30.0, "appetite": 15.0, "current": 45.83, "direction": "lower_better", "cde_ids": ["CDE_DPD"]},
    ],
    "critical_data_elements": [
        {"cde_id": "CDE_OUTSTANDING", "name": "outstanding_balance", "schema": "dw_core", "table": "fact_loan", "column": "outstanding_balance", "owner": "Зээлийн хэлтэс", "steward": "Credit Steward", "validation": ">= 0", "kri_links": ["KRI_NPL"]},
        {"cde_id": "CDE_DPD", "name": "days_past_due", "schema": "dw_core", "table": "fact_loan", "column": "days_past_due", "owner": "Эрсдэлийн хэлтэс", "steward": "Risk Steward", "validation": ">= 0", "kri_links": ["KRI_NPL", "KRI_DPD_AVG"]},
        {"cde_id": "CDE_NPL_FLAG", "name": "npl_flag", "schema": "dw_core", "table": "fact_loan", "column": "npl_flag", "owner": "Эрсдэлийн хэлтэс", "steward": "Risk Steward", "validation": "TRUE if DPD>=90", "kri_links": ["KRI_NPL"]},
        {"cde_id": "CDE_TIER1", "name": "tier1_capital", "schema": "data_marts", "table": "mart_srep_capital_adequacy", "column": "tier1_capital", "owner": "Санхүү", "steward": "Finance Steward", "validation": "> 0", "kri_links": ["KRI_CAR"]},
        {"cde_id": "CDE_TIER2", "name": "tier2_capital", "schema": "data_marts", "table": "mart_srep_capital_adequacy", "column": "tier2_capital", "owner": "Санхүү", "steward": "Finance Steward", "validation": ">= 0", "kri_links": ["KRI_CAR"]},
        {"cde_id": "CDE_RWA", "name": "risk_weighted_assets", "schema": "data_marts", "table": "mart_srep_capital_adequacy", "column": "risk_weighted_assets", "owner": "Эрсдэл", "steward": "Risk Steward", "validation": "> 0", "kri_links": ["KRI_CAR"]},
        {"cde_id": "CDE_LIQUID", "name": "liquid_assets", "schema": "data_marts", "table": "mart_srep_liquidity", "column": "liquid_assets", "owner": "Treasury", "steward": "Liquidity Steward", "validation": ">= 0", "kri_links": ["KRI_LCR"]},
        {"cde_id": "CDE_ST_LIAB", "name": "short_term_liab", "schema": "data_marts", "table": "mart_srep_liquidity", "column": "short_term_liab", "owner": "Treasury", "steward": "Liquidity Steward", "validation": "> 0", "kri_links": ["KRI_LCR"]},
    ],
}

# ---------------------------------------------------------------------------
# 3.3 Governance roles (1LOD / central DG / 2LOD validation / 3LOD audit)
# ---------------------------------------------------------------------------
GOVERNANCE_ROLES = [
    {"function": "Data Owner", "line": "1LOD", "name": "Зээлийн хэлтэс / Эрсдэл / Санхүү", "duties": ["CDE ownership front-to-end", "DQ controls definition", "Remediation of DQ failures"]},
    {"function": "Data Steward", "line": "1LOD", "name": "Credit / Risk / Finance Stewards", "duties": ["Dictionary & lineage metadata", "Day-to-day DQ monitoring"]},
    {"function": "Central Data Governance", "line": "1LOD/Centre", "name": "Data Governance Office", "duties": ["Policies & standards", "Framework oversight", "Change mgmt with RDARR impact"]},
    {"function": "RDARR Validation", "line": "2LOD", "name": "Risk Independent Validation", "duties": ["Independent assessment of RDARR", "IT/lineage/taxonomy review", "Segregation from producers"]},
    {"function": "Internal Audit", "line": "3LOD", "name": "Дотоод аудит", "duties": ["Periodic independent review", "Validation function oversight"]},
    {"function": "IT / Platform", "line": "1LOD", "name": "DWH & Application team", "duties": ["ETL automation", "Access control", "Audit trail integrity"]},
]

# ---------------------------------------------------------------------------
# 3.4 Attribute-level lineage for CDEs
# ---------------------------------------------------------------------------
ATTRIBUTE_LINEAGE = [
    {
        "cde_id": "CDE_OUTSTANDING",
        "steps": [
            {"order": 1, "layer": "source", "system": "CORE_DB", "object": "LOANS.OUTSTANDING"},
            {"order": 2, "layer": "staging", "system": "DWH", "object": "staging.stg_core_loans.outstanding_balance"},
            {"order": 3, "layer": "core", "system": "DWH", "object": "dw_core.fact_loan.outstanding_balance", "transform": "DQ clean + hash"},
            {"order": 4, "layer": "mart", "system": "DWH", "object": "mart_srep_credit_portfolio.total_outstanding", "transform": "SUM()"},
            {"order": 5, "layer": "report", "system": "PLATFORM", "object": "SREP Dashboard / M1.A.01"},
        ],
    },
    {
        "cde_id": "CDE_DPD",
        "steps": [
            {"order": 1, "layer": "source", "system": "CORE_DB", "object": "LOANS.DAYS_PAST_DUE"},
            {"order": 2, "layer": "staging", "system": "DWH", "object": "staging.stg_core_loans.days_past_due"},
            {"order": 3, "layer": "core", "system": "DWH", "object": "dw_core.fact_loan.days_past_due", "transform": "range check >=0"},
            {"order": 4, "layer": "mart", "system": "DWH", "object": "npl_flag / npl_ratio_pct", "transform": "DPD>=90 → NPL"},
            {"order": 5, "layer": "report", "system": "PLATFORM", "object": "KRI_NPL / KRI_DPD_AVG"},
        ],
    },
    {
        "cde_id": "CDE_RWA",
        "steps": [
            {"order": 1, "layer": "source", "system": "ERP_ACC", "object": "GL risk-weight mapping"},
            {"order": 2, "layer": "staging", "system": "DWH", "object": "stg_acc_journal"},
            {"order": 3, "layer": "core", "system": "DWH", "object": "fact_journal"},
            {"order": 4, "layer": "mart", "system": "DWH", "object": "mart_srep_capital_adequacy.risk_weighted_assets"},
            {"order": 5, "layer": "report", "system": "PLATFORM", "object": "KRI_CAR / M1.B.01"},
        ],
    },
]

# ---------------------------------------------------------------------------
# 3.5 Data quality KPIs, issue register, manual workarounds, reconciliation
# ---------------------------------------------------------------------------
DQ_KPIS = [
    {"dimension": "accuracy", "kpi_code": "DQ_ACC_PASS", "name_mn": "Accuracy — дүрмийн PASS %", "value": 100.0, "tolerance": 98.0, "unit": "%", "status": "OK", "as_of": AS_OF},
    {"dimension": "integrity", "kpi_code": "DQ_INT_HASH", "name_mn": "Integrity — hash/uniqueness fail", "value": 0.0, "tolerance": 0.0, "unit": "rows", "status": "OK", "as_of": AS_OF},
    {"dimension": "completeness", "kpi_code": "DQ_CMP_NULL", "name_mn": "Completeness — mandatory null %", "value": 0.0, "tolerance": 0.5, "unit": "%", "status": "OK", "as_of": AS_OF},
    {"dimension": "timeliness", "kpi_code": "DQ_TIME_ETL", "name_mn": "Timeliness — nightly ETL by 09:00", "value": 1.0, "tolerance": 1.0, "unit": "boolean", "status": "OK", "as_of": AS_OF},
    {"dimension": "timeliness", "kpi_code": "DQ_TIME_PROD", "name_mn": "Report production days (monthly M1)", "value": 3.0, "tolerance": 20.0, "unit": "working_days", "status": "OK", "as_of": AS_OF},
]

DQ_ISSUES = [
    {
        "issue_id": "DQI-2026-001",
        "title": "NPL харьцаа risk appetite-ээс ихээхэн хэтэрсэн (demo portfolio)",
        "severity": "HIGH",
        "status": "OPEN",
        "dimension": "accuracy",
        "affected_kri": "KRI_NPL",
        "root_cause": "Demo seed дээр NPL төвлөрөл өндөр; бодит орчинд Core DPD sync шалгах шаардлагатай",
        "impact_analysis": "Эрсдэлийн профайл / SREP credit pillar буруу ойлголт өгч болзошгүй",
        "owner": "RISK",
        "opened_at": (TODAY - timedelta(days=12)).isoformat(),
        "due_at": (TODAY + timedelta(days=18)).isoformat(),
        "remediation_plan": "Core read-replica холбож DPD/outstanding дахин тооцоолох; portfolio cleanup",
    },
    {
        "issue_id": "DQI-2026-002",
        "title": "IFRS9 ECL загвар scope-д ороогүй",
        "severity": "MEDIUM",
        "status": "OPEN",
        "dimension": "completeness",
        "affected_kri": None,
        "root_cause": "Загварын дата pipeline бэлэн бус",
        "impact_analysis": "Provisioning тайлангийн бүрэн бүтэн байдал хязгаарлагдмал",
        "owner": "FINANCE",
        "opened_at": (TODAY - timedelta(days=40)).isoformat(),
        "due_at": (TODAY + timedelta(days=60)).isoformat(),
        "remediation_plan": "Phase-2 model onboarding (Section 3.2 models)",
    },
]

MANUAL_WORKAROUNDS = [
    {
        "id": "EUC-001",
        "name": "M1 Excel template manual cell check",
        "type": "end_user_computing",
        "in_scope": True,
        "controls": ["four_eyes", "audit_trail_export", "sign_off_REPORT"],
        "owner": "REPORT",
        "status": "CONTROLLED",
        "target_automation": "OpenPyXL template fill — platform export (done for M1)",
    },
    {
        "id": "EUC-002",
        "name": "Ad-hoc liquidity fire-drill spreadsheet",
        "type": "manual_aggregation",
        "in_scope": True,
        "controls": ["four_eyes", "documented_procedure"],
        "owner": "TREASURY",
        "status": "TO_AUTOMATE",
        "target_automation": "Fire-drill API endpoint + mart snapshot",
    },
]

RECONCILIATIONS = [
    {"id": "REC-LOAN-CORE", "source_a": "CORE_DB.LOANS", "source_b": "dw_core.fact_loan", "metric": "count + sum(outstanding)", "last_run": AS_OF, "status": "MATCH", "delta": 0},
    {"id": "REC-GL-CAP", "source_a": "ERP Tier1/Tier2 GL", "source_b": "mart_srep_capital_adequacy", "metric": "tier1+tier2", "last_run": AS_OF, "status": "MATCH", "delta": 0},
    {"id": "REC-M1-MART", "source_a": "mart_srep_credit_portfolio", "source_b": "mart_reg_mongolbank_m1", "metric": "M1.A.01 vs total_outstanding", "last_run": AS_OF, "status": "MATCH", "delta": 0},
]

# ---------------------------------------------------------------------------
# 3.6 Timeliness — reporting calendar + production SLA (+ stress readiness)
# ---------------------------------------------------------------------------
REPORTING_CALENDAR = [
    {"report_id": "RPT_SREP_EXEC", "frequency": "daily", "sla_working_days": 0, "cutoff": "09:00", "last_produced": f"{AS_OF}T08:15:00+08:00", "production_days": 0, "within_sla": True},
    {"report_id": "RPT_CREDIT_PORT", "frequency": "daily", "sla_working_days": 0, "cutoff": "09:00", "last_produced": f"{AS_OF}T08:15:00+08:00", "production_days": 0, "within_sla": True},
    {"report_id": "RPT_M1", "frequency": "monthly", "sla_working_days": 10, "cutoff": "T+10", "last_produced": f"{AS_OF}T10:00:00+08:00", "production_days": 3, "within_sla": True, "ecb_benchmark_max_days": 20},
    {"report_id": "RPT_SZH", "frequency": "monthly", "sla_working_days": 12, "cutoff": "T+12", "last_produced": f"{AS_OF}T11:00:00+08:00", "production_days": 4, "within_sla": True, "ecb_benchmark_max_days": 20},
]

STRESS_CAPABILITY = {
    "fire_drill_ready": True,
    "last_fire_drill": (TODAY - timedelta(days=90)).isoformat(),
    "scenarios": [
        {"code": "FD_CREDIT_CONC", "name": "Credit concentration by customer (ad-hoc)", "granularity": "customer_id", "sla_hours": 4, "last_result": "PASS"},
        {"code": "FD_LIQ", "name": "Liquidity fire drill", "granularity": "entity", "sla_hours": 8, "last_result": "PASS"},
    ],
    "note": "SSM 3.6: stress/ad-hoc aggregation must not be blocked by fragmented IT or heavy manual steps",
}

# ---------------------------------------------------------------------------
# 3.7 Implementation programme
# ---------------------------------------------------------------------------
IMPLEMENTATION_PROGRAMME = {
    "name": "ББСБ RDARR / BCBS 239 Implementation Programme",
    "sponsor": "CRO + CFO",
    "status": "IN_PROGRESS",
    "overall_progress_pct": 42,
    "milestones": [
        {"id": "M1", "title": "Scope & CDE inventory (3.2)", "due": (TODAY - timedelta(days=30)).isoformat(), "status": "DONE", "progress_pct": 100},
        {"id": "M2", "title": "Integrated architecture staging→core→marts (3.4)", "due": (TODAY - timedelta(days=10)).isoformat(), "status": "DONE", "progress_pct": 100},
        {"id": "M3", "title": "DQ KPI + issue register + reconciliation (3.5)", "due": (TODAY + timedelta(days=20)).isoformat(), "status": "IN_PROGRESS", "progress_pct": 70},
        {"id": "M4", "title": "Attribute-level lineage for all CDEs (3.4)", "due": (TODAY + timedelta(days=45)).isoformat(), "status": "IN_PROGRESS", "progress_pct": 40},
        {"id": "M5", "title": "Core/ERP read-replica live ETL (timeliness)", "due": (TODAY + timedelta(days=90)).isoformat(), "status": "PLANNED", "progress_pct": 10},
        {"id": "M6", "title": "2LOD validation & 3LOD audit cycle (3.3)", "due": (TODAY + timedelta(days=120)).isoformat(), "status": "PLANNED", "progress_pct": 5},
        {"id": "M7", "title": "Fire-drill automation & IFRS9 onboarding", "due": (TODAY + timedelta(days=180)).isoformat(), "status": "PLANNED", "progress_pct": 0},
    ],
}

BCBS239_SELF_ASSESSMENT = [
    {"principle": "P1 Governance", "ssm_ref": "3.1/3.3", "score": 3, "max": 5, "gap": "Management pack automated; board training cadence formalize"},
    {"principle": "P2 Data architecture / IT", "ssm_ref": "3.4", "score": 3, "max": 5, "gap": "Attribute lineage partial; live source connectors pending"},
    {"principle": "P3 Accuracy & integrity", "ssm_ref": "3.5", "score": 3, "max": 5, "gap": "Expand automated controls beyond null/range/unique"},
    {"principle": "P4 Completeness", "ssm_ref": "3.2/3.5", "score": 2, "max": 5, "gap": "Climate + IFRS9 models out of scope"},
    {"principle": "P5 Timeliness", "ssm_ref": "3.6", "score": 4, "max": 5, "gap": "Daily dashboards OK; stress drill semi-manual"},
    {"principle": "P6 Adaptability", "ssm_ref": "3.6", "score": 2, "max": 5, "gap": "Ad-hoc fire-drill UI needed"},
    {"principle": "P7 Accuracy of reports", "ssm_ref": "3.5", "score": 3, "max": 5, "gap": "Reconciliation coverage expand"},
    {"principle": "P8 Comprehensiveness", "ssm_ref": "3.2", "score": 3, "max": 5, "gap": "All material risks not yet in marts"},
    {"principle": "P9 Clarity / usefulness", "ssm_ref": "3.1.7", "score": 4, "max": 5, "gap": "Exec pack qualitative commentary"},
    {"principle": "P10 Frequency", "ssm_ref": "3.6", "score": 4, "max": 5, "gap": "Align risk appetite escalation workflow"},
    {"principle": "P11 Distribution", "ssm_ref": "3.3", "score": 3, "max": 5, "gap": "RBAC roles OK; committee distribution list"},
]


def kri_status(kri: dict) -> str:
    cur = float(kri["current"])
    lim = float(kri["limit"])
    if kri["direction"] == "higher_better":
        return "BREACH" if cur < lim else ("WATCH" if cur < float(kri["appetite"]) else "OK")
    return "BREACH" if cur > lim else ("WATCH" if cur > float(kri["appetite"]) else "OK")


def management_pack() -> dict:
    kris = [{**k, "status": kri_status(k)} for k in SCOPE["kris"]]
    return {
        "as_of": AS_OF,
        "guide": "ECB SSM Guide on effective risk data aggregation and risk reporting (May 2024)",
        "management_body": MANAGEMENT_BODY,
        "kri_summary": kris,
        "dq_kpis": DQ_KPIS,
        "open_issues": [i for i in DQ_ISSUES if i["status"] == "OPEN"],
        "timeliness": REPORTING_CALENDAR,
        "programme_progress_pct": IMPLEMENTATION_PROGRAMME["overall_progress_pct"],
        "bcbs239_avg": round(sum(p["score"] for p in BCBS239_SELF_ASSESSMENT) / len(BCBS239_SELF_ASSESSMENT), 2),
    }
