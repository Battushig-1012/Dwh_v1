"""
Operational source reports packs.

Шинэ жижиг тайлан нэмэх:
  1. backend/app/ops_reports/<code>/calc.py  — тооцоолол / demo дата
  2. backend/app/ops_reports/<code>/__init__.py — register(ReportSpec(...))
  3. энэ файлын _load_packs()-д import нэмэх
  4. Sidebar өөрчлөхгүй — /ops-reports каталог автоматаар харуулна
"""

from __future__ import annotations

from .registry import catalog, get, list_reports


def _load_packs() -> None:
    # Pack imports (side-effect registration). Add new packs here.
    # from . import some_pack  # noqa: F401
    pass


_load_packs()

__all__ = ["catalog", "get", "list_reports"]
