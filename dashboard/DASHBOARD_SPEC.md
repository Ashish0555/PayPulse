# Power BI Dashboard Specification

## Page 1 — Executive Reliability
- KPI cards: Total Volume, Weighted TD%, Estimated Technical Failures, Unresolved Reversals
- Scatter: X = TD%, Y = Technical Failed Mn, bubble size = Volume, label = Bank
- Bar: Top 10 banks by absolute technical failures
- Quadrant legend: ACT_NOW / FIX_RATE / WATCH_SCALE / LOWER_PRIORITY

## Page 2 — Rate vs Scale
- Paired rank table: TD-rate rank vs absolute-failure rank
- Pareto chart: technical failures + cumulative share
- Matrix: Bank × Approved% / BD% / TD% / reversal success
- Slicer: priority quadrant

## Page 3 — Ecosystem Context
- Line: monthly UPI volume, Apr–Aug 2026
- Line: average transaction value
- Column: live banks
- Payer vs Payee weighted TD comparison
- Explicit snapshot-date and limitations text box
