"""
EBA/GL/2019/04 — Guidelines on ICT and security risk management (29 Nov 2019).
Additive pack for the DWH/reporting platform (does not replace SSM/BCBS RDARR screens).
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

TODAY = date.today()
AS_OF = TODAY.isoformat()

# In-memory privileged activity log (3.4.2.d) — appended at runtime
PRIVILEGED_ACCESS_LOG: list[dict] = []

ICT_STRATEGY = {
    "title": "ББСБ ICT & Security Strategy (aligned to business / RDARR)",
    "approved_by": "Management body",
    "approved_at": (TODAY - timedelta(days=60)).isoformat(),
    "aligned_to_business": True,
    "objectives": [
        "Protect confidentiality, integrity, availability of risk & regulatory data",
        "Support RDARR / BCBS 239 reporting under normal and stress conditions",
        "Reduce ICT operational & cyber risk to appetite",
        "Ensure recoverable DWH/API/UI within defined RTO/RPO",
    ],
    "action_plans": [
        {"id": "AP-01", "measure": "Enforce MFA for privileged accounts", "owner": "CISO / IT", "due": (TODAY + timedelta(days=45)).isoformat(), "status": "IN_PROGRESS"},
        {"id": "AP-02", "measure": "Complete annual BCP restore drill for DWH", "owner": "IT Ops", "due": (TODAY + timedelta(days=90)).isoformat(), "status": "PLANNED"},
        {"id": "AP-03", "measure": "Vulnerability scan + patch cycle for platform hosts", "owner": "SecOps", "due": (TODAY + timedelta(days=30)).isoformat(), "status": "IN_PROGRESS"},
        {"id": "AP-04", "measure": "Third-party assurance for cloud/hosting (if used)", "owner": "Procurement + Risk", "due": (TODAY + timedelta(days=120)).isoformat(), "status": "PLANNED"},
    ],
}

GOVERNANCE = {
    "management_body_accountable": True,
    "roles": [
        {"role": "Management body", "duty": "Approve ICT strategy & information security policy; oversee ICT risk (¶2–4)"},
        {"role": "CISO / InfoSec", "duty": "Information security policy, monitoring, testing, awareness (¶28–49)"},
        {"role": "ICT Operations", "duty": "Asset inventory, logging, backup, capacity, incidents (¶50–60)"},
        {"role": "2LOD Risk / Compliance", "duty": "Oversee ICT risk framework independence from ICT ops (¶10–11)"},
        {"role": "3LOD Internal Audit", "duty": "Independent ICT/security audits; follow-up (¶25–27)"},
        {"role": "Data / RDARR owners", "duty": "Business ownership of information assets feeding reports"},
    ],
    "three_lines_note": "Guidelines are compatible with three lines of defence; ICT ops ≠ control function oversight.",
}

# 3.3.2 / 3.5 — asset inventory with CIA classification & interdependencies
ICT_ASSETS = [
    {"asset_id": "AST-PG-DWH", "name": "PostgreSQL DWH", "type": "database", "owner": "IT Ops", "location": "On-prem / DC", "cia": {"C": "High", "I": "High", "A": "High"}, "criticality": "CRITICAL", "depends_on": ["AST-NET-CORE"], "supports": ["AST-API", "AST-ETL"], "lifecycle": "supported", "patch_status": "current"},
    {"asset_id": "AST-API", "name": "FastAPI reporting API", "type": "application", "owner": "App team", "location": "App tier", "cia": {"C": "High", "I": "High", "A": "High"}, "criticality": "CRITICAL", "depends_on": ["AST-PG-DWH", "AST-NET-CORE"], "supports": ["AST-UI"], "lifecycle": "supported", "patch_status": "current"},
    {"asset_id": "AST-UI", "name": "Next.js RDARR UI", "type": "application", "owner": "App team", "location": "App tier", "cia": {"C": "Medium", "I": "Medium", "A": "Medium"}, "criticality": "IMPORTANT", "depends_on": ["AST-API"], "supports": [], "lifecycle": "supported", "patch_status": "current"},
    {"asset_id": "AST-ETL", "name": "Python / Airflow ETL", "type": "batch", "owner": "Data Eng", "location": "App tier", "cia": {"C": "High", "I": "High", "A": "Medium"}, "criticality": "CRITICAL", "depends_on": ["AST-PG-DWH", "AST-SRC-CORE"], "supports": ["AST-PG-DWH"], "lifecycle": "supported", "patch_status": "current"},
    {"asset_id": "AST-SRC-CORE", "name": "Core Banking read-replica link", "type": "interface", "owner": "IT + Credit", "location": "Source network", "cia": {"C": "High", "I": "High", "A": "Medium"}, "criticality": "CRITICAL", "depends_on": ["AST-NET-CORE"], "supports": ["AST-ETL"], "lifecycle": "supported", "patch_status": "vendor"},
    {"asset_id": "AST-NET-CORE", "name": "Internal VLAN / firewall zone", "type": "network", "owner": "Network", "location": "DC", "cia": {"C": "High", "I": "High", "A": "High"}, "criticality": "CRITICAL", "depends_on": [], "supports": ["AST-PG-DWH", "AST-API"], "lifecycle": "supported", "patch_status": "current"},
]

# 3.3.3 risk assessment summary
RISK_REGISTER = [
    {"risk_id": "ICT-R-01", "threat": "Unauthorised privileged access to DWH", "asset": "AST-PG-DWH", "likelihood": "Medium", "impact": "High", "residual": "Medium", "mitigation": "Least privilege, MFA plan, privileged logging, recertification"},
    {"risk_id": "ICT-R-02", "threat": "Ransomware / data encryption attack", "asset": "AST-PG-DWH", "likelihood": "Medium", "impact": "High", "residual": "Medium", "mitigation": "Offline/remote backups, restore tests, network segmentation"},
    {"risk_id": "ICT-R-03", "threat": "ETL failure → stale risk reports", "asset": "AST-ETL", "likelihood": "Medium", "impact": "Medium", "residual": "Low", "mitigation": "Monitoring, DQ timeliness KPI, incident process"},
    {"risk_id": "ICT-R-04", "threat": "Third-party hosting / SaaS outage", "asset": "AST-API", "likelihood": "Low", "impact": "High", "residual": "Medium", "mitigation": "Contractual SLA, exit plan, BCP alternate site"},
    {"risk_id": "ICT-R-05", "threat": "Insider misuse of regulatory export", "asset": "AST-API", "likelihood": "Low", "impact": "High", "residual": "Low", "mitigation": "RBAC, export audit trail, distribution classification"},
]

INFORMATION_SECURITY_POLICY = {
    "version": "1.0",
    "approved_by": "Management body",
    "approved_at": (TODAY - timedelta(days=60)).isoformat(),
    "principles": ["Confidentiality", "Integrity", "Availability"],
    "applies_to": ["staff", "contractors", "processes", "technology"],
    "scope_note": "Covers risk/regulatory data at rest, in transit, and in use on the RDARR platform.",
    "measures": ["organisation_governance", "logical_security", "physical_security", "operations_security", "security_monitoring", "testing", "awareness"],
}

# 3.4.2 logical access
LOGICAL_ACCESS = {
    "principles": ["need_to_know", "least_privilege", "segregation_of_duties", "user_accountability"],
    "authentication": {
        "standard_users": "complex_password (demo); MFA planned for production",
        "privileged_users": "MFA required (action plan AP-01)",
        "remote_admin": "need-to-know + strong authentication",
    },
    "roles_matrix": [
        {"username": "ceo", "role": "EXEC", "privileged": False, "systems": ["UI dashboard", "RDARR pack"]},
        {"username": "risk", "role": "RISK", "privileged": False, "systems": ["UI all risk views", "API read"]},
        {"username": "report", "role": "REPORT", "privileged": False, "systems": ["Regulatory export"]},
        {"username": "auditor", "role": "AUDITOR", "privileged": False, "systems": ["Read-only lineage/DQ/audit"]},
        {"username": "admin", "role": "ADMIN", "privileged": True, "systems": ["All API", "user admin (future)"]},
    ],
    "recertification": {
        "frequency": "quarterly",
        "last_review": (TODAY - timedelta(days=20)).isoformat(),
        "next_review": (TODAY + timedelta(days=70)).isoformat(),
        "findings": ["No excessive privileges found in demo role set", "Generic shared accounts: none"],
    },
}

PHYSICAL_SECURITY = {
    "scope": "Data centre / server room hosting DWH (on-prem)",
    "controls": ["badge access", "visitor logging", "CCTV", "environmental (UPS, fire, HVAC)"],
    "last_access_review": (TODAY - timedelta(days=40)).isoformat(),
    "note": "Physical controls owned by facilities/IT; platform documents requirements only.",
}

# 3.4.4 / 3.4.5 operations + monitoring
OPERATIONS_SECURITY = {
    "vulnerability_mgmt": "Monthly scans; critical patches within 14 days",
    "network": ["segmentation (DB not internet-facing)", "TLS in transit (prod)", "DLP evaluation planned"],
    "endpoint": "Hardened baselines before network join",
    "encryption": "At rest (disk/TDE planned); in transit TLS 1.2+",
    "change_linkage": "Security-impacting changes go through ICT change process (¶37, ¶75)",
}

SECURITY_MONITORING = {
    "capabilities": [
        "Privileged user activity logging (API)",
        "Failed login anomaly review",
        "Export/audit trail monitoring",
        "ETL job failure alerts",
        "Threat intel / vulnerability watch (process)",
    ],
    "coverage": ["internal admin functions", "third-party access misuse detection", "CIA breach indicators"],
}

# 3.4.6 testing
SECURITY_TESTING = {
    "framework": "Risk-based; independent testers for critical systems annually",
    "tests": [
        {"id": "TST-2026-01", "type": "vulnerability_scan", "target": "API + UI hosts", "date": (TODAY - timedelta(days=25)).isoformat(), "result": "PASS_WITH_FINDINGS", "severity_open": 2},
        {"id": "TST-2026-02", "type": "config_review", "target": "PostgreSQL hardening", "date": (TODAY - timedelta(days=50)).isoformat(), "result": "PASS", "severity_open": 0},
        {"id": "TST-2026-03", "type": "penetration_test", "target": "External attack surface", "date": (TODAY - timedelta(days=200)).isoformat(), "result": "SCHEDULED", "severity_open": None, "note": "Annual critical system test"},
    ],
}

# 3.4.7 awareness
AWARENESS = {
    "programme": "Annual information security awareness for all staff/contractors",
    "last_campaign": (TODAY - timedelta(days=80)).isoformat(),
    "coverage_pct": 92,
    "topics": ["phishing", "data classification", "acceptable use", "incident reporting"],
}

# 3.5 backup / capacity
OPERATIONS = {
    "backup": {
        "scope": "PostgreSQL DWH + config repos",
        "frequency": "Daily full + WAL/archive",
        "offsite": True,
        "last_restore_test": (TODAY - timedelta(days=100)).isoformat(),
        "restore_test_result": "PASS",
        "rpo_hours": 24,
        "rto_hours": 4,
    },
    "capacity": {
        "cpu_pct": 35,
        "disk_pct": 42,
        "status": "OK",
        "last_reviewed": AS_OF,
    },
    "logging": "Critical ICT ops + privileged access retained per criticality (demo: in-memory + audit_trail concept)",
}

# 3.5.1 incidents
INCIDENTS = [
    {
        "incident_id": "INC-2026-014",
        "title": "ETL nightly job delayed (demo)",
        "category": "operational",
        "priority": "P3",
        "status": "CLOSED",
        "detected_at": (TODAY - timedelta(days=5)).isoformat(),
        "resolved_at": (TODAY - timedelta(days=5)).isoformat(),
        "impact": "Dashboard freshness delayed <2h",
        "root_cause": "Resource contention on batch host",
        "lessons": "Added capacity alert threshold",
        "escalated_to_mgmt": False,
    },
    {
        "incident_id": "INC-2026-021",
        "title": "Repeated failed admin login attempts",
        "category": "security",
        "priority": "P2",
        "status": "MONITORING",
        "detected_at": (TODAY - timedelta(days=1)).isoformat(),
        "resolved_at": None,
        "impact": "No successful breach; account lockout policy triggered",
        "root_cause": "Under investigation (possible credential stuffing)",
        "lessons": "Pending",
        "escalated_to_mgmt": True,
    },
]

INCIDENT_PROCESS = {
    "classification_criteria": ["business criticality", "CIA impact", "customer/regulatory impact"],
    "early_warning": ["failed privileged logins spike", "ETL SLA breach", "disk >85%", "backup failure"],
    "escalation": "Significant incidents → senior ICT mgmt ad hoc; management body informed for significant events (¶60.d)",
    "external_comms": "Supervisory/customer notices per regulation when applicable",
}

# 3.2.3 third parties
THIRD_PARTIES = [
    {"id": "TP-01", "name": "Core Banking vendor (read-replica access)", "service": "Data source", "criticality": "HIGH", "assurance": "Contractual security clauses + access review", "exit_plan": True},
    {"id": "TP-02", "name": "ERP / Accounting provider", "service": "GL extract", "criticality": "HIGH", "assurance": "Annual SOC/assurance request", "exit_plan": True},
    {"id": "TP-03", "name": "Optional cloud IaaS (if used)", "service": "Hosting", "criticality": "HIGH", "assurance": "Pending — action AP-04", "exit_plan": True},
]

# 3.6 change / projects
ICT_CHANGES = [
    {"change_id": "CHG-104", "title": "Enable DEMO_MODE API security headers", "risk": "Low", "security_review": True, "tested": True, "approved_by": "IT Change Board", "status": "DONE", "date": (TODAY - timedelta(days=10)).isoformat()},
    {"change_id": "CHG-110", "title": "Add privileged access logging endpoint", "risk": "Medium", "security_review": True, "tested": True, "approved_by": "CISO delegate", "status": "DONE", "date": AS_OF},
    {"change_id": "CHG-118", "title": "Production MFA for admin", "risk": "High", "security_review": True, "tested": False, "approved_by": "Pending", "status": "PLANNED", "date": (TODAY + timedelta(days=45)).isoformat()},
]

ICT_PROJECTS = [
    {"project_id": "PRJ-RDARR", "name": "RDARR / DWH platform", "status": "IN_PROGRESS", "security_requirements_embedded": True, "reported_to_mgmt": True},
    {"project_id": "PRJ-IAM", "name": "IAM / MFA rollout", "status": "PLANNED", "security_requirements_embedded": True, "reported_to_mgmt": True},
]

# 3.7 BCM / BIA (ICT focus — complements BCBS BCP pack)
BIA = [
    {"function": "SREP / KRI dashboard availability", "max_tolerable_downtime_h": 4, "rto_h": 4, "rpo_h": 24, "critical_assets": ["AST-API", "AST-UI", "AST-PG-DWH"]},
    {"function": "Nightly ETL / mart refresh", "max_tolerable_downtime_h": 24, "rto_h": 8, "rpo_h": 24, "critical_assets": ["AST-ETL", "AST-PG-DWH", "AST-SRC-CORE"]},
    {"function": "Regulatory M1 export", "max_tolerable_downtime_h": 48, "rto_h": 12, "rpo_h": 24, "critical_assets": ["AST-API", "AST-PG-DWH"]},
]

BCM = {
    "scenarios": ["cyber attack", "DC outage", "ransomware", "key vendor failure", "data corruption"],
    "last_bcp_test": (TODAY - timedelta(days=100)).isoformat(),
    "bcp_test_result": "PASS_WITH_FINDINGS",
    "crisis_comms": ["internal crisis tree", "regulator contact list", "customer notice templates (if needed)"],
    "update_cycle": "At least annually + after material tests/incidents (¶88)",
}

# 3.3.6 / 3.3.5 audit & reporting
AUDIT = {
    "last_ict_audit": (TODAY - timedelta(days=150)).isoformat(),
    "plan_approved_by_mgmt_body": True,
    "open_findings": [
        {"id": "AUD-ICT-07", "title": "MFA not yet enforced for privileged accounts", "severity": "HIGH", "due": (TODAY + timedelta(days=45)).isoformat()},
        {"id": "AUD-ICT-11", "title": "Formalise security monitoring SIEM use-cases", "severity": "MEDIUM", "due": (TODAY + timedelta(days=90)).isoformat()},
    ],
    "follow_up_process": "Formal verification & remediation tracking (¶27)",
}

COMPLIANCE_SCORECARD = [
    {"section": "3.1 Proportionality", "status": "APPLIED", "evidence": "NBFI-scale controls; critical path hardened first"},
    {"section": "3.2 Governance & strategy", "status": "PARTIAL", "evidence": "ICT strategy + roles documented in platform"},
    {"section": "3.3 Risk management framework", "status": "PARTIAL", "evidence": "Asset map, CIA class, risk register, audit findings"},
    {"section": "3.4 Information security", "status": "PARTIAL", "evidence": "Policy summary, IAM matrix, monitoring, tests, awareness"},
    {"section": "3.5 ICT operations", "status": "PARTIAL", "evidence": "Inventory, backup/restore, capacity, incidents"},
    {"section": "3.6 Project & change", "status": "PARTIAL", "evidence": "Change log with security review flags"},
    {"section": "3.7 BCM", "status": "PARTIAL", "evidence": "BIA for platform functions + BCP test record"},
    {"section": "3.8 Payment user mgmt", "status": "N/A", "evidence": "Not a PSP payment front — out of platform scope"},
]


def overview() -> dict:
    open_inc = sum(1 for i in INCIDENTS if i["status"] != "CLOSED")
    return {
        "standard": "EBA/GL/2019/04 — Guidelines on ICT and security risk management (29 November 2019)",
        "as_of": AS_OF,
        "scorecard": COMPLIANCE_SCORECARD,
        "open_incidents": open_inc,
        "open_audit_findings": len(AUDIT["open_findings"]),
        "critical_assets": sum(1 for a in ICT_ASSETS if a["criticality"] == "CRITICAL"),
        "strategy_approved_at": ICT_STRATEGY["approved_at"],
    }


def log_privileged_access(username: str, role: str, action: str, detail: str = "") -> None:
    PRIVILEGED_ACCESS_LOG.insert(
        0,
        {
            "ts": datetime.now(timezone.utc).isoformat(),
            "username": username,
            "role": role,
            "action": action,
            "detail": detail,
            "privileged": role in {"ADMIN"} or action.startswith("PRIV_"),
        },
    )
    # keep last 200
    del PRIVILEGED_ACCESS_LOG[200:]
