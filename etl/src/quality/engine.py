"""Data Quality rules engine — null, type/range, uniqueness checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class DQResult:
    rule_code: str
    rule_name: str
    target_table: str
    severity: str
    passed: bool
    failed_rows: int
    total_rows: int
    details: dict[str, Any] = field(default_factory=dict)


class DataQualityEngine:
    def __init__(self, target_table: str):
        self.target_table = target_table
        self.results: list[DQResult] = []

    def null_check(self, df: pd.DataFrame, columns: list[str], severity: str = "CRITICAL") -> pd.DataFrame:
        mask = pd.Series(False, index=df.index)
        for col in columns:
            mask = mask | df[col].isna() | (df[col].astype(str).str.strip() == "")
        failed = int(mask.sum())
        self.results.append(
            DQResult(
                rule_code=f"NULL_{'_'.join(columns).upper()}",
                rule_name=f"Mandatory columns not null: {', '.join(columns)}",
                target_table=self.target_table,
                severity=severity,
                passed=failed == 0,
                failed_rows=failed,
                total_rows=len(df),
                details={"columns": columns},
            )
        )
        return df.loc[~mask].copy()

    def range_check(
        self,
        df: pd.DataFrame,
        column: str,
        min_value: float | None = None,
        max_value: float | None = None,
        severity: str = "ERROR",
    ) -> pd.DataFrame:
        mask = pd.Series(False, index=df.index)
        if min_value is not None:
            mask = mask | (df[column] < min_value)
        if max_value is not None:
            mask = mask | (df[column] > max_value)
        failed = int(mask.sum())
        self.results.append(
            DQResult(
                rule_code=f"RANGE_{column.upper()}",
                rule_name=f"{column} within [{min_value}, {max_value}]",
                target_table=self.target_table,
                severity=severity,
                passed=failed == 0,
                failed_rows=failed,
                total_rows=len(df),
                details={"column": column, "min": min_value, "max": max_value},
            )
        )
        return df.loc[~mask].copy()

    def uniqueness_check(self, df: pd.DataFrame, columns: list[str], severity: str = "ERROR") -> pd.DataFrame:
        dup = df.duplicated(subset=columns, keep="first")
        failed = int(dup.sum())
        self.results.append(
            DQResult(
                rule_code=f"UNIQ_{'_'.join(columns).upper()}",
                rule_name=f"Unique key: {', '.join(columns)}",
                target_table=self.target_table,
                severity=severity,
                passed=failed == 0,
                failed_rows=failed,
                total_rows=len(df),
                details={"columns": columns},
            )
        )
        return df.loc[~dup].copy()

    def has_critical_failures(self) -> bool:
        return any(not r.passed and r.severity == "CRITICAL" for r in self.results)
