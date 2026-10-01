from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "bank_reliability_aug2025.csv"

checks = []


def check(name: str, ok: bool, detail: str = ""):
    checks.append((name, bool(ok), detail))


with DATA_PATH.open(encoding="utf-8", newline="") as fh:
    rows = list(csv.DictReader(fh))

check("rows_present", len(rows) > 0, f"{len(rows)} rows")
check("bank_unique", len({row["bank_name"] for row in rows}) == len(rows))
check(
    "percentages_0_100",
    all(
        0 <= float(row[col]) <= 100
        for row in rows
        for col in ["approved_pct", "business_decline_pct", "technical_decline_pct", "debit_reversal_success_pct"]
    ),
)
check("volume_positive", all(float(row["total_volume_mn"]) > 0 for row in rows))
check(
    "component_sum_near_100",
    all(
        abs(float(row["approved_pct"]) + float(row["business_decline_pct"]) + float(row["technical_decline_pct"]) - 100) <= 0.05
        for row in rows
    ),
)
check("derived_td_nonnegative", all(float(row["technical_failed_mn"]) >= 0 for row in rows))

passed = sum(1 for _, ok, _ in checks if ok)
failed = len(checks) - passed

for name, ok, detail in checks:
    status = "PASS" if ok else "FAIL"
    print(f"{status} {name} {detail}".strip())

print(f"Validation summary: {passed} passed, {failed} failed.")

if failed:
    sys.exit(1)
