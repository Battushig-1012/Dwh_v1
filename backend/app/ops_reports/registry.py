"""
Operational / source reports registry.

Жижиг PRPT, завсрын тайлан, Core тооцооллыг sidebar-д биш энд бүртгэнэ.
Шинэ тайлан = шинэ pack folder + register() — шинэ nav item биш.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class ReportSpec:
    code: str
    title: str
    category: str  # e.g. cash | credit | gl | interim
    source_system: str
    summary: str
    tags: tuple[str, ...] = ()
    ui_path: str = ""  # relative under /ops-reports/{code}
    # Callables return JSON-serializable structures
    overview_fn: Callable[[], dict[str, Any]] | None = None
    mart_fn: Callable[..., dict[str, Any] | list] | None = None
    staging_fn: Callable[[], list] | None = None
    pipeline_fn: Callable[[], dict[str, Any]] | None = None
    sql_fn: Callable[[], dict[str, Any]] | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def catalog_item(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "title": self.title,
            "category": self.category,
            "source_system": self.source_system,
            "summary": self.summary,
            "tags": list(self.tags),
            "href": f"/ops-reports/{self.code}",
            "api_base": f"/api/ops-reports/{self.code}",
        }


_REGISTRY: dict[str, ReportSpec] = {}


def register(spec: ReportSpec) -> ReportSpec:
    key = spec.code.upper()
    if key in _REGISTRY:
        raise ValueError(f"Ops report already registered: {key}")
    _REGISTRY[key] = spec
    return spec


def get(code: str) -> ReportSpec | None:
    return _REGISTRY.get(code.upper())


def list_reports(*, category: str | None = None) -> list[ReportSpec]:
    items = sorted(_REGISTRY.values(), key=lambda s: (s.category, s.code))
    if category:
        c = category.lower()
        items = [s for s in items if s.category.lower() == c]
    return items


def catalog(*, category: str | None = None) -> dict[str, Any]:
    specs = list_reports(category=category)
    cats: dict[str, int] = {}
    for s in specs:
        cats[s.category] = cats.get(s.category, 0) + 1
    return {
        "total": len(specs),
        "categories": cats,
        "reports": [s.catalog_item() for s in specs],
        "convention": {
            "add_pack": "backend/app/ops_reports/<code>/",
            "register": "ops_reports.registry.register(ReportSpec(...))",
            "ui": "/ops-reports — нэг sidebar цэс; дэлгэрэнгүй /ops-reports/{CODE}",
            "api": "/api/ops-reports и /api/ops-reports/{CODE}/*",
        },
    }
