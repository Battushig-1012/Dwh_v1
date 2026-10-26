"""
EBA/GL/2021/05 — Guidelines on internal governance under CRD (2 July 2021).
Additive governance pack for ББСБ platform (does not replace RDARR/ICT/DPM screens).
"""

from __future__ import annotations

from datetime import date, timedelta

TODAY = date.today()
AS_OF = TODAY.isoformat()

STANDARD = "EBA/GL/2021/05 — Guidelines on internal governance under Directive 2013/36/EU (2 July 2021)"

# Title I — Proportionality
PROPORTIONALITY = {
    "applied": True,
    "criteria": ["size", "internal organisation", "nature/scope/complexity of activities", "risk profile"],
    "note": "NBFI-scale: combined risk & audit committee allowed where proportionate (Title II §5.6).",
}

# Title II — Management body & committees
MANAGEMENT_BODY = {
    "structure": "dual_functions_in_one_body",  # common for smaller entities
    "chair": {"name": "Төрсөнбаяр А.", "role": "Chair (supervisory emphasis)", "independent": True},
    "management_function": [
        {"name": "Батбаяр Г.", "role": "CEO / EXEC", "username": "ceo"},
        {"name": "Сараа М.", "role": "CRO", "username": "risk"},
        {"name": "Оюунчимэг Т.", "role": "CFO / Reporting", "username": "report"},
    ],
    "supervisory_function": [
        {"name": "Төрсөнбаяр А.", "role": "Chair"},
        {"name": "Энхтуяа Д.", "role": "Independent member"},
        {"name": "Ганбат С.", "role": "Independent member"},
    ],
    "collective_suitability": {
        "last_assessment": (TODAY - timedelta(days=90)).isoformat(),
        "covers": ["banking/credit", "risk management", "IT/data", "accounting", "AML/compliance"],
        "status": "ADEQUATE",
    },
    "responsibilities_highlights": [
        "Approve and oversee business & risk strategy, internal governance (Art. 88 CRD / GL §1)",
        "Ensure integrity of accounting & reporting systems",
        "Oversee internal control functions and risk culture",
        "Approve RDARR / ICT strategies as part of overall governance",
    ],
}

COMMITTEES = [
    {
        "code": "RISK_COM",
        "name": "Risk Committee (combined with Audit where proportionate)",
        "type": "combined_risk_audit",
        "chair": "Энхтуяа Д.",
        "members": ["Энхтуяа Д.", "Ганбат С.", "Төрсөнбаяр А."],
        "mandate": [
            "Advise on risk appetite and strategy (GL §5.4)",
            "Oversee risk management framework & RDARR reporting quality",
            "Review internal audit plan and significant findings (GL §5.5)",
            "Monitor ICAAP/ILAAP and material risk reports",
        ],
        "meeting_frequency": "quarterly",
        "last_meeting": (TODAY - timedelta(days=25)).isoformat(),
        "next_meeting": (TODAY + timedelta(days=65)).isoformat(),
    },
]

# Title III — Organisational framework / know your structure
ORG_STRUCTURE = {
    "legal_entities": [
        {"code": "BBSB_HQ", "name": "ББСБ төв", "jurisdiction": "MN", "activity": "NBFI lending", "booked": True},
        {"code": "BBSB_BR_UB", "name": "УБ салбар", "jurisdiction": "MN", "activity": "Branch origination", "booked": True},
    ],
    "business_lines": ["Retail/Consumer credit", "SME credit", "Treasury/liquidity"],
    "key_functions": ["CEO", "CRO/RMF", "CFO", "Compliance", "Internal Audit", "IT/CISO", "Credit underwriting"],
    "complex_structures": {
        "present": False,
        "note": "No SPV / non-transparent structures; know-your-structure review annual (GL §6.2–6.3)",
    },
    "group_context": {
        "applies": False,
        "note": "Solo ББСБ — Title III §7 group provisions N/A unless holding structure emerges",
    },
    "outsourcing_policy": {
        "exists": True,
        "last_review": (TODAY - timedelta(days=120)).isoformat(),
        "critical_outsourced": ["Core banking vendor access", "ERP accounting"],
        "link": "See ICT module third-party register (EBA/GL/2019/04 ¶7–9 + IG §8)",
    },
}

# Title IV — Risk culture & conduct
RISK_CULTURE = {
    "tone_from_top": "Management body promotes risk awareness within appetite; breaches escalated",
    "principles": ["accountability", "effective communication", "challenge", "incentives aligned with risk"],
    "code_of_conduct": {
        "version": "2.1",
        "approved_at": (TODAY - timedelta(days=180)).isoformat(),
        "topics": ["ethics", "market conduct", "data confidentiality", "AML", "gifts & hospitality"],
        "last_attestation_pct": 96,
    },
}

CONFLICTS_OF_INTEREST = [
    {
        "case_id": "COI-2026-03",
        "type": "staff",
        "party": "Credit officer — related borrower application",
        "status": "MITIGATED",
        "control": "Recusal + four-eyes approval by independent manager",
        "recorded_at": (TODAY - timedelta(days=40)).isoformat(),
    },
    {
        "case_id": "COI-2026-01",
        "type": "management_body_related_party_loan",
        "party": "Loan to related party of supervisory member (documentation file)",
        "status": "DOCUMENTED",
        "control": "Board disclosure + arm's-length terms + Compliance review (GL §12.1–12.2)",
        "recorded_at": (TODAY - timedelta(days=200)).isoformat(),
    },
]

WHISTLEBLOWING = {
    "internal_alert_channels": ["secure email", "anonymous web form", "Compliance officer"],
    "protects_whistleblowers": True,
    "last_case": None,
    "training_last": (TODAY - timedelta(days=70)).isoformat(),
    "reporting_to_authority": "Procedure exists for breaches to competent authority (GL §14)",
}

# Title V — Internal control / three lines
THREE_LINES = [
    {
        "line": "1LOD",
        "name": "Business / Front-to-back operations",
        "units": ["Credit underwriting", "Collections", "Finance ops", "IT ops", "Reporting production"],
        "duty": "Own and manage risks; implement controls; accurate data entry",
    },
    {
        "line": "2LOD",
        "name": "Independent control functions",
        "units": ["Risk Management Function (RMF/CRO)", "Compliance"],
        "duty": "Monitor, challenge, advise; independent from business lines (GL §19–21)",
    },
    {
        "line": "3LOD",
        "name": "Internal Audit",
        "units": ["Internal Audit"],
        "duty": "Independent assurance on governance, risk & controls including 1LOD & 2LOD (GL §22)",
    },
]

CONTROL_FUNCTIONS = [
    {
        "function": "Risk Management Function",
        "head": "Сараа М. (CRO)",
        "reports_to": "Management body / Risk Committee",
        "independent": True,
        "combined_with": None,
        "resources": "Adequate for NBFI scale",
        "key_duties": [
            "Risk strategy & appetite (GL §20.1)",
            "Identify/measure/monitor/mitigate/report risks (GL §20.3)",
            "Material changes & new products challenge (GL §18, §20.2)",
            "RDARR risk data quality oversight",
        ],
    },
    {
        "function": "Compliance",
        "head": "Nominated Compliance Officer",
        "reports_to": "Management body",
        "independent": True,
        "combined_with": None,
        "resources": "Shared specialist support + external counsel as needed",
        "key_duties": ["Legal/regulatory compliance monitoring", "Conduct & COI", "Whistleblowing intake"],
    },
    {
        "function": "Internal Audit",
        "head": "Эрдэнэ Б. (Audit lead)",
        "reports_to": "Audit/Risk Committee & management body",
        "independent": True,
        "combined_with": None,
        "resources": "Risk-based annual plan; external co-source for ICT",
        "key_duties": ["Risk-based audits", "Follow-up of findings", "Review of RDARR/ICT controls"],
    },
]

NEW_PRODUCTS = {
    "policy_exists": True,
    "process": "New Product Approval Committee (NPAC): Business → Risk → Compliance → IT → Board if material",
    "recent": [
        {
            "id": "NPA-2026-02",
            "product": "SME revolving facility enhancement",
            "status": "APPROVED_WITH_CONDITIONS",
            "risk_opinion": "Concentration limits tightened",
            "date": (TODAY - timedelta(days=55)).isoformat(),
        }
    ],
}

INTERNAL_CONTROL_FRAMEWORK = {
    "documented": True,
    "covers": ["credit", "liquidity", "operational/ICT", "compliance", "financial reporting"],
    "risk_management_framework": "Integrated with appetite, KRIs, ICAAP-lite for NBFI",
    "last_mgmt_review": (TODAY - timedelta(days=30)).isoformat(),
}

# Title VI — BCM (pointer + governance ownership; detail in ICT module)
BCM_GOVERNANCE = {
    "owned_by": "Management body oversight; IT Ops execution",
    "policy_approved": True,
    "detail_module": "/ict (BCM tab) + /bcbs BCP",
    "last_test_ref": "See ICT BCM last_bcp_test",
}

# Title VII — Transparency
TRANSPARENCY = {
    "internal": [
        "Clear org chart & reporting lines published internally",
        "Committee mandates & minutes retained",
        "Risk & audit findings tracked to closure",
    ],
    "external": [
        "Regulatory reporting via DPM/M1 hub",
        "Supervisory disclosure as required by local rules",
        "No complex opaque structures to disclose",
    ],
    "website_governance_summary": "Planned — high-level governance statement",
}

SCORECARD = [
    {"title": "I Proportionality", "status": "APPLIED", "evidence": "Combined committee; NBFI-scaled control functions"},
    {"title": "II Management body & committees", "status": "PARTIAL", "evidence": "Body composition, combined Risk/Audit committee register"},
    {"title": "III Governance framework / KYS", "status": "PARTIAL", "evidence": "Legal entities, business lines, outsourcing policy link"},
    {"title": "IV Risk culture & conduct", "status": "PARTIAL", "evidence": "Code of conduct, COI cases, whistleblowing channels"},
    {"title": "V Internal control / 3LOD", "status": "PARTIAL", "evidence": "RMF/Compliance/IA mandates; NPAC"},
    {"title": "VI Business continuity", "status": "LINKED", "evidence": "Governance ownership → ICT BCM detail"},
    {"title": "VII Transparency", "status": "PARTIAL", "evidence": "Internal transparency practices; external disclosures via reporting hub"},
]

MEETING_PACK = {
    "as_of": AS_OF,
    "for_committee": "RISK_COM",
    "agenda_items": [
        "KRI / risk appetite breaches (link /rdarr, /kri)",
        "DQ & ICT open findings",
        "COI & conduct update",
        "Internal audit follow-ups",
        "New product pipeline",
    ],
}


def overview() -> dict:
    return {
        "standard": STANDARD,
        "as_of": AS_OF,
        "scorecard": SCORECARD,
        "proportionality": PROPORTIONALITY,
        "open_coi": sum(1 for c in CONFLICTS_OF_INTEREST if c["status"] != "CLOSED"),
        "committee_count": len(COMMITTEES),
        "control_functions": len(CONTROL_FUNCTIONS),
    }
