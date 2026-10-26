"""
BCBS 239 (Jan 2013) — Principles for effective RDARR.
Only additive content vs SSM May 2024 pack (no duplicate of SSM 3.1–3.7 UI data).
"""

from __future__ import annotations

from datetime import date, timedelta

TODAY = date.today()
AS_OF = TODAY.isoformat()

# ---------------------------------------------------------------------------
# Official 14 principles compliance matrix (Annex 2)
# Scores reuse prior self-assessment where overlapping; expand P7–P14 gaps.
# ---------------------------------------------------------------------------
PRINCIPLES = [
    {"id": "P1", "section": "I Governance & infrastructure", "title": "Governance",
     "summary": "Strong governance for RDARR; board oversight; independent validation; change/acquisition impact",
     "score": 3, "max": 5, "status": "PARTIAL", "covered_by": ["RDARR Pack", "Programme / 3LOD"],
     "gap": "Formal board sign-off workflow & periodic independent validation cycle"},
    {"id": "P2", "section": "I Governance & infrastructure", "title": "Data architecture & IT infrastructure",
     "summary": "Architecture supports normal + stress; integrated taxonomy; single identifiers; BCP",
     "score": 3, "max": 5, "status": "PARTIAL", "covered_by": ["staging→core→marts", "Dictionary", "Lineage"],
     "gap": "Live BCP test evidence; full single-ID rollout across all sources"},
    {"id": "P3", "section": "II Aggregation", "title": "Accuracy & Integrity",
     "summary": "Accurate aggregation, largely automated; EUC controls; reconciliation; authoritative sources",
     "score": 3, "max": 5, "status": "PARTIAL", "covered_by": ["DQ engine", "EUC register", "Reconciliation"],
     "gap": "Expand automated controls; authoritative source per risk fully enforced"},
    {"id": "P4", "section": "II Aggregation", "title": "Completeness",
     "summary": "All material risks; by business line, entity, asset, industry, region; concentrations",
     "score": 2, "max": 5, "status": "PARTIAL", "covered_by": ["Scope inventory"],
     "gap": "Off-balance sheet & climate; richer concentration dimensions"},
    {"id": "P5", "section": "II Aggregation", "title": "Timeliness",
     "summary": "Up-to-date aggregate data; timing by risk volatility; stress speed for critical risks",
     "score": 4, "max": 5, "status": "STRONG", "covered_by": ["Timeliness SLA", "Nightly ETL"],
     "gap": "Intraday critical credit/liquidity feeds"},
    {"id": "P6", "section": "II Aggregation", "title": "Adaptability",
     "summary": "On-demand / ad-hoc aggregation; stress queries; drill-down; regulatory change",
     "score": 3, "max": 5, "status": "PARTIAL", "covered_by": ["Fire-drill API"],
     "gap": "Broader ad-hoc dimensions & supervisory query templates"},
    {"id": "P7", "section": "III Reporting", "title": "Accuracy (reports)",
     "summary": "Reports reconciled/validated; edit checks; exception reports; approximation standards",
     "score": 3, "max": 5, "status": "PARTIAL", "covered_by": ["Export audit", "DQ rules"],
     "gap": "Report-level validation inventory & precision requirements formalized"},
    {"id": "P8", "section": "III Reporting", "title": "Comprehensiveness",
     "summary": "All material risk areas; limits/appetite context; emerging concentrations; forward-looking",
     "score": 3, "max": 5, "status": "PARTIAL", "covered_by": ["SREP dashboard", "KRI"],
     "gap": "Unified comprehensive risk report + forecasts"},
    {"id": "P9", "section": "III Reporting", "title": "Clarity & usefulness",
     "summary": "Clear, concise, recipient-tailored; qualitative + quantitative balance; periodic confirmation",
     "score": 3, "max": 5, "status": "PARTIAL", "covered_by": ["RDARR Pack"],
     "gap": "Board vs management report variants & recipient attestation"},
    {"id": "P10", "section": "III Reporting", "title": "Frequency",
     "summary": "Frequency set by recipients & risk dynamics; increase in stress",
     "score": 4, "max": 5, "status": "STRONG", "covered_by": ["Reporting calendar"],
     "gap": "Documented stress frequency escalation matrix"},
    {"id": "P11", "section": "III Reporting", "title": "Distribution",
     "summary": "Timely distribution to relevant parties; confidentiality maintained",
     "score": 2, "max": 5, "status": "PARTIAL", "covered_by": ["RBAC roles"],
     "gap": "Distribution lists, classification, delivery confirmation"},
    {"id": "P12", "section": "IV Supervisory", "title": "Supervisory review",
     "summary": "Supervisors review compliance; short-deadline information tests",
     "score": 3, "max": 5, "status": "EVIDENCE", "covered_by": ["Fire-drill", "Export pack"],
     "gap": "Supervisory evidence pack export (readiness)"},
    {"id": "P13", "section": "IV Supervisory", "title": "Remedial actions",
     "summary": "Supervisors require timely remediation of deficiencies",
     "score": 3, "max": 5, "status": "EVIDENCE", "covered_by": ["Issue register", "Programme"],
     "gap": "Link supervisory findings IDs to milestones"},
    {"id": "P14", "section": "IV Supervisory", "title": "Home/host cooperation",
     "summary": "Cross-border supervisor cooperation (less relevant for solo ББСБ)",
     "score": 4, "max": 5, "status": "N/A-LIGHT", "covered_by": ["Single-entity scope"],
     "gap": "N/A unless cross-border subsidiaries expand"},
]

# P1 — limitations, trade-offs, expert judgment, materiality, change checklist
LIMITATIONS = [
    {"id": "LIM-001", "type": "technical", "description": "Core/ERP live connectors not yet connected (DEMO sources)", "impact": "Aggregation relies on demo/seed extracts", "accepted_by": "CRO", "review_date": (TODAY + timedelta(days=30)).isoformat()},
    {"id": "LIM-002", "type": "coverage", "description": "Climate risk & IFRS9 ECL models out of RDARR scope (phase-2)", "impact": "Comprehensiveness gap on non-financial / provisioning", "accepted_by": "Board Risk Committee", "review_date": (TODAY + timedelta(days=90)).isoformat()},
    {"id": "LIM-003", "type": "manual", "description": "Liquidity fire-drill semi-manual spreadsheet residual", "impact": "Adaptability partially dependent on EUC", "accepted_by": "CFO", "review_date": (TODAY + timedelta(days=60)).isoformat()},
]

TRADEOFFS = [
    {"id": "TO-001", "context": "Urgent ad-hoc credit concentration request", "principles_relaxed": ["P3 automation"], "mitigation": "Four-eyes + documented export", "board_aware": True},
]

EXPERT_JUDGMENTS = [
    {"id": "EJ-001", "date": (TODAY - timedelta(days=20)).isoformat(), "topic": "Watch-list mapping for borderline DPD 30–89", "rationale": "Policy aligns status_code WATCH with DPD band", "reviewer": "Risk Validation (2LOD)", "documented": True},
]

MATERIALITY_POLICY = {
    "definition": "Omission/misstatement is material if it could influence board/senior management risk decisions (BCBS ¶23).",
    "examples": ["KRI breach misstated", "Top-10 borrower exposure wrong", "CAR misstated > 0.5pp"],
    "exceptions_log_required": True,
}

CHANGE_CHECKLIST = [
    {"item": "New product / process", "rdarr_impact_assessed": True, "owner": "Product + Risk"},
    {"item": "IT change / tool upgrade", "rdarr_impact_assessed": True, "owner": "IT + DG Office"},
    {"item": "Acquisition / divestiture", "rdarr_impact_assessed": False, "owner": "Board", "note": "No active M&A"},
    {"item": "Outsourcing of data process", "rdarr_impact_assessed": True, "owner": "CRO"},
]

# P2 — single identifiers, authoritative sources, BCP
SINGLE_IDENTIFIERS = [
    {"entity": "Customer", "id_field": "customer_id", "convention": "C###", "authoritative_system": "LOAN_APP / CORE_DB", "status": "ACTIVE"},
    {"entity": "Loan", "id_field": "loan_id", "convention": "L####", "authoritative_system": "CORE_DB", "status": "ACTIVE"},
    {"entity": "Legal entity", "id_field": "legal_entity_code", "convention": "BBSB_*", "authoritative_system": "Governance scope", "status": "ACTIVE"},
    {"entity": "GL account", "id_field": "account_code", "convention": "numeric chart", "authoritative_system": "ERP_ACC", "status": "ACTIVE"},
]

AUTHORITATIVE_SOURCES = [
    {"risk_type": "CREDIT", "authoritative_source": "CORE_DB loans + dw_core.fact_loan", "notes": "Single source per credit exposure"},
    {"risk_type": "CAPITAL", "authoritative_source": "ERP GL → mart_srep_capital_adequacy", "notes": "Reconciled to finance"},
    {"risk_type": "LIQUIDITY", "authoritative_source": "ERP liquid assets → mart_srep_liquidity", "notes": "Simplified LCR"},
    {"risk_type": "OPERATIONAL", "authoritative_source": "TBD incident register", "notes": "Phase-2"},
]

BCP_RDARR = {
    "in_bcp": True,
    "last_bia": (TODAY - timedelta(days=120)).isoformat(),
    "rto_hours_critical_reports": 4,
    "rpo_hours_dwh": 24,
    "last_test": (TODAY - timedelta(days=180)).isoformat(),
    "result": "PASS_WITH_FINDINGS",
    "finding": "Failover runbook for API tier documented; DWH restore drill annual",
}

# P3/P7 — validation rules inventory + accuracy requirements + escalation
VALIDATION_RULES_INVENTORY = [
    {"rule_id": "VR-NULL-LOAN", "applies_to": "stg_core_loans.loan_id", "logic": "NOT NULL", "type": "completeness", "automated": True},
    {"rule_id": "VR-RANGE-RATE", "applies_to": "interest_rate", "logic": ">= 0", "type": "accuracy", "automated": True},
    {"rule_id": "VR-UNIQ-LOAN", "applies_to": "loan_id", "logic": "UNIQUE", "type": "integrity", "automated": True},
    {"rule_id": "VR-NPL-FLAG", "applies_to": "npl_flag", "logic": "DPD>=90 ↔ TRUE", "type": "logical", "automated": True},
    {"rule_id": "VR-M1-RECON", "applies_to": "M1.A.01 vs mart total_outstanding", "logic": "ABS(delta)=0", "type": "report_recon", "automated": True},
    {"rule_id": "VR-CAR-FORMULA", "applies_to": "car_pct", "logic": "total_capital/RWA*100", "type": "report_check", "automated": True},
]

ACCURACY_REQUIREMENTS = {
    "normal": {"kri_tolerance_pct_points": 0.1, "exposure_tolerance_mnt": 1000, "report_recon_required": True},
    "stress": {"kri_tolerance_pct_points": 0.5, "exposure_tolerance_mnt": 10000, "report_recon_required": True, "note": "Wider tolerance only if board-approved"},
}

DQ_ESCALATION = [
    {"severity": "CRITICAL", "channel": "Immediate to CRO + DG Office", "sla_hours": 4},
    {"severity": "HIGH", "channel": "Risk Committee weekly pack", "sla_hours": 48},
    {"severity": "MEDIUM", "channel": "Steward backlog", "sla_hours": 120},
]

# P4 — completeness by dimension + concentration slices
COMPLETENESS_MATRIX = [
    {"dimension": "legal_entity", "coverage_pct": 100, "exception": None},
    {"dimension": "business_line", "coverage_pct": 100, "exception": None},
    {"dimension": "product", "coverage_pct": 100, "exception": None},
    {"dimension": "branch_region", "coverage_pct": 100, "exception": None},
    {"dimension": "off_balance_sheet", "coverage_pct": 0, "exception": "Not yet in DWH — documented gap"},
    {"dimension": "industry_sector", "coverage_pct": 40, "exception": "Industry code partial on borrowers"},
]

CONCENTRATIONS = {
    "by_customer": [
        {"customer_id": "C004", "name": "Номин Эрдэнэ", "outstanding": 38_000_000, "share_pct": 47.2, "npl": True},
        {"customer_id": "C002", "name": "Сарнай Бат", "outstanding": 24_800_000, "share_pct": 30.8, "npl": True},
        {"customer_id": "C001", "name": "Болд Дорж", "outstanding": 16_500_000, "share_pct": 20.5, "npl": False},
        {"customer_id": "C003", "name": "Төмөр Ган", "outstanding": 1_200_000, "share_pct": 1.5, "npl": False},
    ],
    "by_product": [
        {"product_code": "SME", "outstanding": 60_000_000, "share_pct": 74.5},
        {"product_code": "CONS", "outstanding": 11_500_000, "share_pct": 14.3},
        {"product_code": "AUTO", "outstanding": 9_000_000, "share_pct": 11.2},
    ],
    "by_branch": [
        {"branch_code": "DN01", "outstanding": 38_000_000, "share_pct": 47.2},
        {"branch_code": "UB02", "outstanding": 24_800_000, "share_pct": 30.8},
        {"branch_code": "UB01", "outstanding": 17_700_000, "share_pct": 22.0},
    ],
    "emerging_risk_note": "Single-name concentration C004 > 40% of portfolio — action: reduce / collateral review",
}

# P8/P9 — comprehensive risk report + recipient profiles + qualitative
FORWARD_LOOKING = {
    "horizon": "6M",
    "scenarios": [
        {"name": "Base", "car_pct": 17.5, "npl_pct": 48.0, "lcr_pct": 125.0, "narrative": "Mild NPL improvement if collections strengthen"},
        {"name": "Adverse", "car_pct": 14.2, "npl_pct": 58.0, "lcr_pct": 105.0, "narrative": "Stress on SME book; LCR still above limit"},
        {"name": "Severe", "car_pct": 12.1, "npl_pct": 65.0, "lcr_pct": 95.0, "narrative": "LCR breach risk; capital near regulatory minimum"},
    ],
    "recommended_actions": [
        "Accelerate NPL recovery / write-off policy for L1004/L1006",
        "Tighten SME underwriting limit pending concentration reduction",
        "Pre-arrange liquidity buffer if Severe path materialises",
    ],
}

RECIPIENT_PROFILES = [
    {
        "recipient": "Board / Risk Committee",
        "needs": ["KRI vs appetite", "Qualitative narrative", "Forward-looking scenarios", "Open CRITICAL/HIGH issues"],
        "detail_level": "highly_aggregated",
        "qual_vs_quant": "qualitative_heavy",
        "last_confirmation": (TODAY - timedelta(days=35)).isoformat(),
        "confirmed_relevant": True,
    },
    {
        "recipient": "Senior management (CRO/CFO)",
        "needs": ["Full KRI pack", "DQ KPIs", "Programme status", "Concentration drill-downs"],
        "detail_level": "aggregated_with_drill",
        "qual_vs_quant": "balanced",
        "last_confirmation": (TODAY - timedelta(days=14)).isoformat(),
        "confirmed_relevant": True,
    },
    {
        "recipient": "Risk analysts",
        "needs": ["Loan-level", "Lineage", "DQ rule fails", "Ad-hoc extracts"],
        "detail_level": "granular",
        "qual_vs_quant": "quantitative_heavy",
        "last_confirmation": (TODAY - timedelta(days=7)).isoformat(),
        "confirmed_relevant": True,
    },
]

# P10 — stress frequency escalation
FREQUENCY_MATRIX = [
    {"report": "Credit single-name / top exposures", "normal": "daily", "stress": "intraday / on-demand", "bcbs_ref": "P5/P10 critical credit"},
    {"report": "Liquidity / LCR", "normal": "daily", "stress": "intraday", "bcbs_ref": "P5 liquidity indicators"},
    {"report": "Capital / CAR", "normal": "daily snapshot / monthly deep", "stress": "daily", "bcbs_ref": "P8/P10"},
    {"report": "SREP executive pack", "normal": "daily dashboard + monthly committee", "stress": "daily + ad-hoc board", "bcbs_ref": "P10"},
    {"report": "Supervisory M1", "normal": "monthly", "stress": "as required by authority", "bcbs_ref": "P10/P12"},
]

# P11 — distribution & confidentiality
DISTRIBUTION = [
    {"report_id": "RPT_SREP_EXEC", "classification": "Confidential", "recipients": ["ceo", "risk", "report", "auditor"], "channel": "Platform UI", "last_delivered": f"{AS_OF}T08:30:00+08:00", "ack_required": True, "acks": ["risk", "ceo"]},
    {"report_id": "RPT_M1", "classification": "Restricted", "recipients": ["report", "auditor", "ceo"], "channel": "Excel export + audit trail", "last_delivered": f"{AS_OF}T10:00:00+08:00", "ack_required": True, "acks": ["report"]},
    {"report_id": "RPT_CREDIT_PORT", "classification": "Internal", "recipients": ["risk", "report"], "channel": "Platform UI", "last_delivered": f"{AS_OF}T08:15:00+08:00", "ack_required": False, "acks": []},
]

APPROXIMATIONS = [
    {"id": "APX-LCR", "description": "Simplified LCR (liquid assets / short-term liab)", "reliability": "indicative", "accuracy_expectation": "Stress tolerance per ACCURACY_REQUIREMENTS.stress", "owner": "Treasury"},
    {"id": "APX-FWD", "description": "6M scenario CAR/NPL/LCR paths", "reliability": "management_estimate", "accuracy_expectation": "Directional only", "owner": "CRO"},
]


def principles_overview() -> dict:
    avg = round(sum(p["score"] for p in PRINCIPLES) / len(PRINCIPLES), 2)
    return {
        "standard": "BCBS 239 — Principles for effective risk data aggregation and risk reporting (January 2013)",
        "as_of": AS_OF,
        "average_score": avg,
        "principles": PRINCIPLES,
        "note": "SSM May 2024 pack remains the operational RDARR UI; this module adds BCBS-native gaps only.",
    }


def comprehensive_risk_report() -> dict:
    return {
        "as_of": AS_OF,
        "title": "Comprehensive internal risk report (BCBS P8/P9)",
        "qualitative_summary": (
            "Demo portfolio shows elevated NPL driven by two SME exposures. "
            "Capital and LCR remain above regulatory minima. "
            "Priority is concentration reduction and collections; forward paths show Severe scenario nearing CAR floor."
        ),
        "risk_areas": [
            {"code": "CREDIT", "status": "BREACH_APPETITE", "commentary": "NPL and single-name concentration elevated"},
            {"code": "CAPITAL", "status": "OK", "commentary": "CAR 18.1% vs 12% minimum"},
            {"code": "LIQUIDITY", "status": "OK", "commentary": "LCR 133% vs 100%"},
            {"code": "OPERATIONAL", "status": "MONITOR", "commentary": "IT/data BCP findings open"},
        ],
        "concentrations": CONCENTRATIONS,
        "forward_looking": FORWARD_LOOKING,
        "approximations_used": APPROXIMATIONS,
        "recipient_guidance": "Use Board profile for committee; analyst drill-downs via Concentration / Lineage screens",
    }
