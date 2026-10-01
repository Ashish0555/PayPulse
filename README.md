# PayPulse — UPI Reliability Economics

PayPulse is a decision-support analysis of UPI reliability using published NPCI ecosystem statistics. The goal is not to explain every payment failure at the transaction level, but to help an operations or risk team decide where to focus attention when the failure rate is poor and the failure scale is large.

## Why this project matters
In payment operations, percentage failures and total failed transactions often tell different stories. A small bank can look alarming on a rate basis while a large bank can be operationally more important in absolute terms. This project separates those two lenses:

- failure rate tells us whether reliability is structurally weak
- failure volume tells us whether the issue is operationally material

That distinction is essential for product, risk, and operations prioritization.

## Business question
Which institutions deserve attention first when UPI reliability degrades: banks with the worst technical-decline rate, or banks generating the largest technical-failure burden on scale?

## What the analysis includes
- bank-level reliability and decline decomposition
- derived technical-failure estimates from published volume and decline rates
- rank comparisons between technical-decline rate and absolute failure burden
- Pareto concentration analysis
- payer/payee PSP-side comparisons
- monthly system trend review for volume, value and average ticket size

## Data sources
- NPCI UPI ecosystem statistics
- NPCI UPI product statistics
- NPCI P2P/P2M snapshot data

Official references:
- https://www.npci.org.in/what-we-do/upi/upi-ecosystem-statistics
- https://www.npci.org.in/product/upi/product-statistics

> The packaged CSVs are a compact analytical snapshot transcribed from public NPCI tables. NPCI remains the authoritative source for production-grade reporting.

## Methodology and assumptions
This project uses a derived estimate:

technical_failed_mn = total_volume_mn × technical_decline_pct / 100

This is a useful proxy for operational burden, not a transaction log. It allows us to compare banks on a common scale while staying within the published data boundaries. Business Declines and Technical Declines are kept separate because they usually imply different remediation actions.

## Prioritization logic
- ACT_NOW: TD ≥ 1% and above-median derived failure impact
- FIX_RATE: TD ≥ 1% and lower derived impact
- WATCH_SCALE: TD < 1% but above-median derived impact
- LOWER_PRIORITY: lower rate and lower derived impact

This is not a one-size-fits-all severity framework. It reflects the operational reality that large institutions can create major service recovery workloads without looking like the worst performers on a percentage basis.

## Repository structure
```text
paypulse-upi-reliability/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── prepare_data.py
│   ├── quality_checks.py
│   └── run_analysis.py
├── sql/
│   ├── schema.sql
│   └── analysis.sql
├── dashboard/
│   ├── model/
│   ├── MEASURES.md
│   └── DASHBOARD_SPEC.md
├── charts/
├── reports/
├── DATA_DICTIONARY.md
├── INTERVIEW_PREP.md
├── LIMITATIONS.md
├── README.md
├── requirements.txt
├── run_all.sh
├── SOURCES.md
└── RESUME_BULLETS.md
```

## Reproduction
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash run_all.sh
```

## Output artifacts
The project generates:
- processed CSVs in data/processed/
- a SQLite database in data/processed/paypulse.sqlite
- ranked summary CSVs in reports/
- an analyst memo and dashboard-ready model tables

## What this project does not claim
- it does not prove causality at the transaction or merchant level
- it does not estimate revenue loss without retry-chain and ticket-size data
- it does not attribute failures to a specific root cause without response-code detail
- it is intended for triage and prioritization, not as a final operational diagnosis

## Realistic use case
This project is best used as a first-pass operating review for a UPI reliability team. It helps answer: where do we deploy investigation effort first, which institutions need immediate remediation, and which institutions warrant monitoring because their scale creates outsized operational burden even when their rate is moderate?
