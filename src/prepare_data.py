from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(name: str):
    path = RAW / name
    if not path.exists():
        raise FileNotFoundError(f"Missing source file: {path}")
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(value):
    return float(value)


def write_csv(path: Path, rows):
    if not rows:
        raise ValueError(f"No rows available to write to {path}")
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    rem = read_csv("remitter_aug2025.csv")
    enriched = []
    for row in rem:
        volume = num(row["total_volume_mn"])
        technical_decline = num(row["technical_decline_pct"])
        business_decline = num(row["business_decline_pct"])
        approved_pct = num(row["approved_pct"])
        reversal_count = num(row["debit_reversal_count_mn"])
        reversal_success = num(row["debit_reversal_success_pct"])

        enriched.append(
            {
                **row,
                "month": "2025-08",
                "approved_volume_mn": round(volume * approved_pct / 100, 4),
                "technical_failed_mn": round(volume * technical_decline / 100, 4),
                "business_failed_mn": round(volume * business_decline / 100, 4),
                "total_failed_mn": round(volume * (technical_decline + business_decline) / 100, 4),
                "unresolved_reversal_mn": round(reversal_count * (1 - reversal_success / 100), 4),
                "td_target_breach": int(technical_decline >= 1.0),
                "bd_target_breach": int(business_decline >= 5.0),
            }
        )

    enriched.sort(key=lambda x: x["technical_failed_mn"], reverse=True)
    total_td = sum(r["technical_failed_mn"] for r in enriched)
    cumulative = 0.0
    for index, record in enumerate(enriched, start=1):
        cumulative += record["technical_failed_mn"]
        record["td_absolute_rank"] = index
        record["td_failure_share_pct"] = round(100 * record["technical_failed_mn"] / total_td, 2)
        record["td_cumulative_share_pct"] = round(100 * cumulative / total_td, 2)

    rate_rank = {
        record["bank_name"]: index
        for index, record in enumerate(
            sorted(enriched, key=lambda x: float(x["technical_decline_pct"]), reverse=True),
            start=1,
        )
    }

    impacts = sorted(float(record["technical_failed_mn"]) for record in enriched)
    median_impact = impacts[len(impacts) // 2]

    for record in enriched:
        record["td_rate_rank"] = rate_rank[record["bank_name"]]
        td = float(record["technical_decline_pct"])
        impact = float(record["technical_failed_mn"])
        if td >= 1 and impact >= median_impact:
            record["priority_quadrant"] = "ACT_NOW"
        elif td >= 1:
            record["priority_quadrant"] = "FIX_RATE"
        elif impact >= median_impact:
            record["priority_quadrant"] = "WATCH_SCALE"
        else:
            record["priority_quadrant"] = "LOWER_PRIORITY"

    write_csv(OUT / "bank_reliability_aug2025.csv", enriched)

    psp_all = []
    for side in ("payer", "payee"):
        rows = []
        for row in read_csv(f"{side}_psp_aug2025.csv"):
            volume = num(row["total_volume_mn"])
            technical_decline = num(row["technical_decline_pct"])
            business_decline = num(row["business_decline_pct"])
            approved_pct = num(row["approved_pct"])
            record = {
                **row,
                "month": "2025-08",
                "side": side,
                "technical_failed_mn": round(volume * technical_decline / 100, 4),
                "business_failed_mn": round(volume * business_decline / 100, 4),
                "approved_volume_mn": round(volume * approved_pct / 100, 4),
            }
            rows.append(record)
            psp_all.append(record)
        write_csv(OUT / f"{side}_psp_aug2025.csv", rows)

    macro = []
    previous = None
    for row in read_csv("upi_macro_2026.csv"):
        volume = num(row["volume_mn"])
        value = num(row["value_cr"])
        record = {**row, "avg_txn_value_inr": round((value / volume) * 100, 2)}
        if previous:
            previous_volume = num(previous["volume_mn"])
            previous_value = num(previous["value_cr"])
            record["volume_mom_pct"] = round((volume - previous_volume) / previous_volume * 100, 2)
            record["value_mom_pct"] = round((value - previous_value) / previous_value * 100, 2)
            record["banks_mom_change"] = int(float(row["banks_live"]) - float(previous["banks_live"]))
        else:
            record["volume_mom_pct"] = ""
            record["value_mom_pct"] = ""
            record["banks_mom_change"] = ""
        macro.append(record)
        previous = row
    write_csv(OUT / "upi_macro_2026_enriched.csv", macro)

    db = OUT / "paypulse.sqlite"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executescript(
        """
        CREATE TABLE bank_reliability (
            month TEXT,
            bank_name TEXT,
            total_volume_mn REAL,
            approved_pct REAL,
            business_decline_pct REAL,
            technical_decline_pct REAL,
            debit_reversal_count_mn REAL,
            debit_reversal_success_pct REAL,
            approved_volume_mn REAL,
            technical_failed_mn REAL,
            business_failed_mn REAL,
            total_failed_mn REAL,
            unresolved_reversal_mn REAL,
            td_target_breach INTEGER,
            bd_target_breach INTEGER,
            td_absolute_rank INTEGER,
            td_failure_share_pct REAL,
            td_cumulative_share_pct REAL,
            td_rate_rank INTEGER,
            priority_quadrant TEXT
        );
        CREATE TABLE psp_performance (
            month TEXT,
            side TEXT,
            psp_name TEXT,
            total_volume_mn REAL,
            approved_pct REAL,
            business_decline_pct REAL,
            technical_decline_pct REAL,
            technical_failed_mn REAL,
            business_failed_mn REAL,
            approved_volume_mn REAL
        );
        CREATE TABLE upi_macro (
            month TEXT,
            banks_live INTEGER,
            volume_mn REAL,
            value_cr REAL,
            avg_txn_value_inr REAL,
            volume_mom_pct REAL,
            value_mom_pct REAL,
            banks_mom_change INTEGER
        );
        """
    )

    for record in enriched:
        cur.execute(
            "INSERT INTO bank_reliability VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                record["month"],
                record["bank_name"],
                num(record["total_volume_mn"]),
                num(record["approved_pct"]),
                num(record["business_decline_pct"]),
                num(record["technical_decline_pct"]),
                num(record["debit_reversal_count_mn"]),
                num(record["debit_reversal_success_pct"]),
                record["approved_volume_mn"],
                record["technical_failed_mn"],
                record["business_failed_mn"],
                record["total_failed_mn"],
                record["unresolved_reversal_mn"],
                record["td_target_breach"],
                record["bd_target_breach"],
                record["td_absolute_rank"],
                record["td_failure_share_pct"],
                record["td_cumulative_share_pct"],
                record["td_rate_rank"],
                record["priority_quadrant"],
            ),
        )

    for record in psp_all:
        cur.execute(
            "INSERT INTO psp_performance VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                record["month"],
                record["side"],
                record["psp_name"],
                num(record["total_volume_mn"]),
                num(record["approved_pct"]),
                num(record["business_decline_pct"]),
                num(record["technical_decline_pct"]),
                record["technical_failed_mn"],
                record["business_failed_mn"],
                record["approved_volume_mn"],
            ),
        )

    for record in macro:
        cur.execute(
            "INSERT INTO upi_macro VALUES (?,?,?,?,?,?,?,?)",
            (
                record["month"],
                int(record["banks_live"]),
                num(record["volume_mn"]),
                num(record["value_cr"]),
                record["avg_txn_value_inr"],
                None if record["volume_mom_pct"] == "" else record["volume_mom_pct"],
                None if record["value_mom_pct"] == "" else record["value_mom_pct"],
                None if record["banks_mom_change"] == "" else record["banks_mom_change"],
            ),
        )

    con.commit()
    con.close()
    print(f"Prepared {len(enriched)} bank records, {len(psp_all)} PSP rows, and {len(macro)} macro observations.")


if __name__ == "__main__":
    main()
