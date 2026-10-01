from pathlib import Path
import sqlite3,csv
ROOT=Path(__file__).resolve().parents[1]; DB=ROOT/'data/processed/paypulse.sqlite'; OUT=ROOT/'reports'; OUT.mkdir(exist_ok=True)
con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
queries={
'priority_banks':"SELECT bank_name,total_volume_mn,technical_decline_pct,technical_failed_mn,td_rate_rank,td_absolute_rank,priority_quadrant FROM bank_reliability ORDER BY technical_failed_mn DESC LIMIT 10",
'pareto':"SELECT bank_name,technical_failed_mn,td_failure_share_pct,td_cumulative_share_pct FROM bank_reliability ORDER BY td_absolute_rank",
'psp_summary':"SELECT side,ROUND(SUM(total_volume_mn),2) volume_mn,ROUND(SUM(technical_failed_mn),2) technical_failed_mn,ROUND(100.0*SUM(technical_failed_mn)/SUM(total_volume_mn),3) weighted_td_pct FROM psp_performance GROUP BY side",
'macro_mom':"SELECT month,banks_live,volume_mn,value_cr,avg_txn_value_inr,volume_mom_pct,value_mom_pct,LAG(volume_mn) OVER(ORDER BY month) prior_volume FROM upi_macro ORDER BY month"}
for name,q in queries.items():
    rows=[dict(r) for r in con.execute(q)]
    with open(OUT/f'{name}.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('Wrote analysis CSVs')
