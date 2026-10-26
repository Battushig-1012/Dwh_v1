"""
EBA Data Point Model (DPM) database description — August 2013.
Demo meta-model for ББСБ Mongolbank M1 (+ SREP link), proportionate to NBFI MVP.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import date

from . import demo_data

AS_OF = date.today().isoformat()
PERIOD = date.today().strftime("%Y-%m")

# ---------------------------------------------------------------------------
# Framework / Taxonomy / Module / Table layout
# ---------------------------------------------------------------------------
FRAMEWORK = {
    "framework_id": 1,
    "framework_code": "MN_REG",
    "framework_label": "Mongolia Regulatory Reporting (ББСБ)",
}

TAXONOMY = {
    "taxonomy_id": 1,
    "framework_id": 1,
    "taxonomy_code": "MN_REG_2026",
    "taxonomy_label": "MN Regulatory Taxonomy 2026",
    "from_date": "2026-01-01",
    "to_date": None,
}

MODULE = {
    "module_id": 1,
    "taxonomy_id": 1,
    "module_code": "M1_MONTHLY",
    "module_label": "Монголбанк M1 — сарын тайлан",
    "default_frequency": "monthly",
}

TABLE = {
    "table_id": 1,
    "framework_id": 1,
    "table_code": "M1",
    "table_label": "Mongolbank M1 Credit & Capital snapshot",
}

TABLE_VERSION = {
    "table_vid": 1,
    "table_id": 1,
    "table_code": "M1.00",
    "table_group": "Credit & Capital",
    "from_date": "2026-01-01",
    "to_date": None,
}

AXES = [
    {"axis_id": 1, "table_vid": 1, "axis_orientation": "Y", "axis_label": "Rows", "axis_order": 1, "is_open_axis": False},
    {"axis_id": 2, "table_vid": 1, "axis_orientation": "X", "axis_label": "Columns", "axis_order": 2, "is_open_axis": False},
]

# ---------------------------------------------------------------------------
# Domains / Dimensions / Members / Metrics
# ---------------------------------------------------------------------------
DOMAINS = [
    {"domain_id": 1, "domain_code": "MET", "domain_label": "Metric", "is_typed_domain": False},
    {"domain_id": 2, "domain_code": "BAS", "domain_label": "Base", "is_typed_domain": False},
    {"domain_id": 3, "domain_code": "MCAT", "domain_label": "Main category", "is_typed_domain": False},
    {"domain_id": 4, "domain_code": "RSK", "domain_label": "Risk type", "is_typed_domain": False},
]

DIMENSIONS = [
    {"dimension_id": 1, "domain_id": 1, "dimension_code": "METRIC", "dimension_label": "Metric", "is_typed": False},
    {"dimension_id": 2, "domain_id": 2, "dimension_code": "BASE", "dimension_label": "Base", "is_typed": False},
    {"dimension_id": 3, "domain_id": 3, "dimension_code": "MAIN_CAT", "dimension_label": "Main category", "is_typed": False},
    {"dimension_id": 4, "domain_id": 4, "dimension_code": "RISK_TYPE", "dimension_label": "Risk type", "is_typed": False},
]

MEMBERS = [
    # Metric domain
    {"member_id": 101, "domain_id": 1, "member_code": "x1", "member_label": "Carrying amount / Outstanding", "is_default_member": False},
    {"member_id": 102, "domain_id": 1, "member_code": "x2", "member_label": "Ratio / Percentage", "is_default_member": False},
    # Base
    {"member_id": 201, "domain_id": 2, "member_code": "ba", "member_label": "Assets / Loans", "is_default_member": False},
    {"member_id": 202, "domain_id": 2, "member_code": "bc", "member_label": "Capital", "is_default_member": False},
    # Main category
    {"member_id": 301, "domain_id": 3, "member_code": "mc1", "member_label": "Total loans", "is_default_member": False},
    {"member_id": 302, "domain_id": 3, "member_code": "mc2", "member_label": "NPL loans", "is_default_member": False},
    {"member_id": 303, "domain_id": 3, "member_code": "mc3", "member_label": "NPL ratio", "is_default_member": False},
    {"member_id": 304, "domain_id": 3, "member_code": "mc4", "member_label": "Capital adequacy ratio", "is_default_member": False},
    # Risk type
    {"member_id": 401, "domain_id": 4, "member_code": "cr", "member_label": "Credit risk", "is_default_member": False},
    {"member_id": 402, "domain_id": 4, "member_code": "ca", "member_label": "Capital adequacy", "is_default_member": False},
]

METRICS = [
    {"metric_id": 101, "data_type": "monetary", "period_type": "instant"},
    {"metric_id": 102, "data_type": "percent", "period_type": "instant"},
]

HIERARCHY = {
    "hierarchy_id": 1,
    "domain_id": 3,
    "hierarchy_code": "MCAT_H1",
    "hierarchy_label": "Loan quality roll-up",
    "nodes": [
        {"member_id": 301, "parent_member_id": None, "order": 1, "level": 1, "path": "301.", "unary_operator": "+"},
        {"member_id": 302, "parent_member_id": 301, "order": 2, "level": 2, "path": "301.302.", "unary_operator": "+"},
        {"member_id": 303, "parent_member_id": 301, "order": 3, "level": 2, "path": "301.303.", "unary_operator": None},
    ],
}

# ---------------------------------------------------------------------------
# Axis ordinates (rows + one amount column)
# ---------------------------------------------------------------------------
def _cat_key(pairs: list[tuple[str, str]]) -> str:
    return "|".join(f"[{d}].[{m}]" for d, m in sorted(pairs))


ORDINATES = [
    # Y rows
    {
        "ordinate_id": 11,
        "axis_id": 1,
        "ordinate_code": "010",
        "ordinate_label": "Нийт зээлийн үлдэгдэл",
        "business_code": "M1.A.01",
        "is_abstract_header": False,
        "metric_id": 101,
        "order": 1,
        "level": 1,
        "path": "11.",
        "categorisation": [("METRIC", "x1"), ("BASE", "ba"), ("MAIN_CAT", "mc1"), ("RISK_TYPE", "cr")],
    },
    {
        "ordinate_id": 12,
        "axis_id": 1,
        "ordinate_code": "020",
        "ordinate_label": "Чанаргүй зээлийн үлдэгдэл",
        "business_code": "M1.A.02",
        "is_abstract_header": False,
        "metric_id": 101,
        "order": 2,
        "level": 1,
        "path": "12.",
        "categorisation": [("METRIC", "x1"), ("BASE", "ba"), ("MAIN_CAT", "mc2"), ("RISK_TYPE", "cr")],
    },
    {
        "ordinate_id": 13,
        "axis_id": 1,
        "ordinate_code": "030",
        "ordinate_label": "NPL харьцаа (%)",
        "business_code": "M1.A.03",
        "is_abstract_header": False,
        "metric_id": 102,
        "order": 3,
        "level": 1,
        "path": "13.",
        "categorisation": [("METRIC", "x2"), ("BASE", "ba"), ("MAIN_CAT", "mc3"), ("RISK_TYPE", "cr")],
    },
    {
        "ordinate_id": 14,
        "axis_id": 1,
        "ordinate_code": "110",
        "ordinate_label": "Капиталын хүрэлцээ (%)",
        "business_code": "M1.B.01",
        "is_abstract_header": False,
        "metric_id": 102,
        "order": 4,
        "level": 1,
        "path": "14.",
        "categorisation": [("METRIC", "x2"), ("BASE", "bc"), ("MAIN_CAT", "mc4"), ("RISK_TYPE", "ca")],
    },
    # abstract header example
    {
        "ordinate_id": 10,
        "axis_id": 1,
        "ordinate_code": "000",
        "ordinate_label": "A. Зээлийн үзүүлэлт",
        "business_code": None,
        "is_abstract_header": True,
        "metric_id": None,
        "order": 0,
        "level": 0,
        "path": "10.",
        "categorisation": [],
    },
    # X column
    {
        "ordinate_id": 21,
        "axis_id": 2,
        "ordinate_code": "001",
        "ordinate_label": "Amount (MNT / %)",
        "business_code": None,
        "is_abstract_header": False,
        "metric_id": None,
        "order": 1,
        "level": 1,
        "path": "21.",
        "categorisation": [],
    },
]

for o in ORDINATES:
    o["categorisation_key"] = _cat_key(o["categorisation"]) if o["categorisation"] else None


def _member_code_to_id(code: str) -> int:
    return next(m["member_id"] for m in MEMBERS if m["member_code"] == code)


def _dim_code_to_id(code: str) -> int:
    return next(d["dimension_id"] for d in DIMENSIONS if d["dimension_code"] == code)


# Data points discovered from unique categorisation keys (non-abstract rows)
DATA_POINTS: list[dict] = []
DATA_POINT_VERSIONS: list[dict] = []
CONTEXTS: list[dict] = []
CELLS: list[dict] = []

_dp_by_key: dict[str, int] = {}
_next_dp = 1
_next_ctx = 1
_next_cell = 1

for o in ORDINATES:
    if o["axis_id"] != 1 or o["is_abstract_header"] or not o["categorisation"]:
        continue
    key = o["categorisation_key"]
    assert key is not None
    if key not in _dp_by_key:
        dp_id = _next_dp
        _next_dp += 1
        _dp_by_key[key] = dp_id
        # metric vs context split (Appendix 2)
        metric_pair = next(p for p in o["categorisation"] if p[0] == "METRIC")
        context_pairs = [p for p in o["categorisation"] if p[0] != "METRIC"]
        ctx_key = _cat_key(context_pairs)
        ctx_id = _next_ctx
        _next_ctx += 1
        CONTEXTS.append(
            {
                "context_id": ctx_id,
                "context_key": ctx_key,
                "definition": [{"dimension_code": d, "member_code": m} for d, m in context_pairs],
            }
        )
        DATA_POINTS.append({"data_point_id": dp_id, "business_code": o["business_code"]})
        DATA_POINT_VERSIONS.append(
            {
                "data_point_vid": dp_id,
                "data_point_id": dp_id,
                "metric_id": o["metric_id"],
                "metric_member_code": metric_pair[1],
                "context_id": ctx_id,
                "from_date": "2026-01-01",
                "to_date": None,
                "categorisation_key": key,
                "business_code": o["business_code"],
            }
        )
    cell_id = _next_cell
    _next_cell += 1
    CELLS.append(
        {
            "cell_id": cell_id,
            "table_vid": 1,
            "data_point_id": _dp_by_key[key],
            "is_shaded": False,
            "is_row_key": False,
            "business_code": o["business_code"],
            "row_ordinate_id": o["ordinate_id"],
            "col_ordinate_id": 21,
            "row_code": o["ordinate_code"],
            "col_code": "001",
        }
    )

# Grey-shaded example: abstract header x column (not reportable)
CELLS.append(
    {
        "cell_id": _next_cell,
        "table_vid": 1,
        "data_point_id": None,
        "is_shaded": True,
        "is_row_key": False,
        "business_code": None,
        "row_ordinate_id": 10,
        "col_ordinate_id": 21,
        "row_code": "000",
        "col_code": "001",
    }
)

VALIDATION_RULES = [
    {
        "rule_code": "DPM_METRIC_MANDATORY",
        "rule_label": "Every reportable cell must have Metric dimension",
        "expression": "EXISTS categorisation METRIC for non-shaded cells",
        "severity": "ERROR",
    },
    {
        "rule_code": "DPM_NO_DUP_DIM",
        "rule_label": "Same dimension cannot categorise a datapoint twice",
        "expression": "UNIQUE dimension_id per DataPointVersion context+metric",
        "severity": "ERROR",
    },
    {
        "rule_code": "DPM_UNIQUE_CAT_KEY",
        "rule_label": "CategorisationKey unique within taxonomy validity",
        "expression": "UNIQUE(categorisation_key) among active DataPointVersions",
        "severity": "ERROR",
    },
    {
        "rule_code": "VAL_M1_NPL_RATIO",
        "rule_label": "M1.A.03 ≈ M1.A.02 / M1.A.01 * 100",
        "expression": "ABS(A03 - A02/A01*100) < 0.05",
        "severity": "ERROR",
    },
]


def _facts_by_business_code() -> dict[str, float]:
    return {r["dpm_code"]: float(r["amount_mnt"]) for r in demo_data.M1}


def run_consistency_checks() -> list[dict]:
    results = []
    # Metric mandatory
    missing_metric = [
        o for o in ORDINATES if o["axis_id"] == 1 and not o["is_abstract_header"] and not any(d == "METRIC" for d, _ in o["categorisation"])
    ]
    results.append(
        {
            "rule_code": "DPM_METRIC_MANDATORY",
            "passed": len(missing_metric) == 0,
            "detail": f"missing={len(missing_metric)}",
        }
    )
    # Duplicate dims
    dup = False
    for o in ORDINATES:
        dims = [d for d, _ in o["categorisation"]]
        if len(dims) != len(set(dims)):
            dup = True
    results.append({"rule_code": "DPM_NO_DUP_DIM", "passed": not dup, "detail": "ok" if not dup else "duplicate found"})
    # Unique keys
    keys = [v["categorisation_key"] for v in DATA_POINT_VERSIONS]
    results.append(
        {
            "rule_code": "DPM_UNIQUE_CAT_KEY",
            "passed": len(keys) == len(set(keys)),
            "detail": f"keys={len(keys)} unique={len(set(keys))}",
        }
    )
    # Business validation NPL ratio
    facts = _facts_by_business_code()
    a01, a02, a03 = facts.get("M1.A.01"), facts.get("M1.A.02"), facts.get("M1.A.03")
    if a01 and a02 is not None and a03 is not None and a01 != 0:
        expected = round(a02 / a01 * 100, 4)
        ok = abs(expected - a03) < 0.05
        results.append(
            {
                "rule_code": "VAL_M1_NPL_RATIO",
                "passed": ok,
                "detail": f"reported={a03} expected≈{expected}",
            }
        )
    else:
        results.append({"rule_code": "VAL_M1_NPL_RATIO", "passed": False, "detail": "missing facts"})
    return results


def overview() -> dict:
    return {
        "standard": "EBA Data Point Model database description (August 2013)",
        "as_of": AS_OF,
        "framework": FRAMEWORK,
        "taxonomy": TAXONOMY,
        "module": MODULE,
        "table": TABLE,
        "table_version": TABLE_VERSION,
        "counts": {
            "domains": len(DOMAINS),
            "dimensions": len(DIMENSIONS),
            "members": len(MEMBERS),
            "ordinates": len(ORDINATES),
            "data_points": len(DATA_POINTS),
            "cells": len(CELLS),
            "reportable_cells": sum(1 for c in CELLS if not c["is_shaded"]),
            "shaded_cells": sum(1 for c in CELLS if c["is_shaded"]),
        },
        "consistency": run_consistency_checks(),
    }


def table_render() -> dict:
    """Render M1 as DPM table: rows (Y) x columns (X) with datapoint + fact."""
    facts = _facts_by_business_code()
    rows = []
    for o in sorted([x for x in ORDINATES if x["axis_id"] == 1], key=lambda z: z["order"]):
        cell = next((c for c in CELLS if c["row_ordinate_id"] == o["ordinate_id"]), None)
        amount = facts.get(o["business_code"]) if o["business_code"] else None
        rows.append(
            {
                "ordinate_code": o["ordinate_code"],
                "ordinate_label": o["ordinate_label"],
                "business_code": o["business_code"],
                "is_abstract_header": o["is_abstract_header"],
                "is_shaded": bool(cell and cell["is_shaded"]),
                "data_point_id": cell["data_point_id"] if cell else None,
                "categorisation_key": o["categorisation_key"],
                "categorisation": [{"dimension": d, "member": m} for d, m in o["categorisation"]],
                "amount": amount,
            }
        )
    return {
        "table_version": TABLE_VERSION,
        "axes": AXES,
        "columns": [{"ordinate_code": "001", "ordinate_label": "Amount (MNT / %)"}],
        "rows": rows,
    }


def datapoint_detail(data_point_id: int) -> dict | None:
    dp = next((d for d in DATA_POINTS if d["data_point_id"] == data_point_id), None)
    if not dp:
        return None
    ver = next(v for v in DATA_POINT_VERSIONS if v["data_point_id"] == data_point_id)
    ctx = next(c for c in CONTEXTS if c["context_id"] == ver["context_id"])
    cells = [c for c in CELLS if c["data_point_id"] == data_point_id]
    facts = _facts_by_business_code()
    amount = facts.get(dp["business_code"]) if dp.get("business_code") else None
    return {
        "data_point": dp,
        "version": ver,
        "context": ctx,
        "cells": cells,
        "fact": {"reporting_period": PERIOD, "amount": amount, "currency": "MNT"},
        "lineage_note": "Fact sourced from data_marts.mart_reg_mongolbank_m1 / demo_data.M1",
    }


def browse_dictionary() -> dict:
    return {
        "domains": DOMAINS,
        "dimensions": DIMENSIONS,
        "members": MEMBERS,
        "metrics": METRICS,
        "hierarchy": HIERARCHY,
        "validation_rules": VALIDATION_RULES,
    }


def enriched_m1_facts() -> list[dict]:
    """M1 facts joined to DPM datapoint ids for Regulatory Hub."""
    out = []
    for row in demo_data.M1:
        dp = next((d for d in DATA_POINTS if d.get("business_code") == row["dpm_code"]), None)
        ver = next((v for v in DATA_POINT_VERSIONS if dp and v["data_point_id"] == dp["data_point_id"]), None)
        out.append(
            {
                **row,
                "data_point_id": dp["data_point_id"] if dp else None,
                "categorisation_key": ver["categorisation_key"] if ver else None,
            }
        )
    return out
