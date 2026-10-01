-- PayPulse analysis queries (SQLite-compatible)

-- 1) Rate vs scale ranking gap
WITH ranked AS (
  SELECT bank_name, total_volume_mn, technical_decline_pct, technical_failed_mn,
         RANK() OVER (ORDER BY technical_decline_pct DESC) AS rate_rank,
         RANK() OVER (ORDER BY technical_failed_mn DESC) AS absolute_rank
  FROM bank_reliability
)
SELECT *, rate_rank - absolute_rank AS rank_gap
FROM ranked
ORDER BY absolute_rank;

-- 2) Pareto concentration of technical failures
WITH x AS (
  SELECT bank_name, technical_failed_mn,
         SUM(technical_failed_mn) OVER () AS total_td,
         SUM(technical_failed_mn) OVER (
           ORDER BY technical_failed_mn DESC
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
         ) AS cumulative_td
  FROM bank_reliability
)
SELECT bank_name, technical_failed_mn,
       ROUND(100.0*technical_failed_mn/total_td,2) AS share_pct,
       ROUND(100.0*cumulative_td/total_td,2) AS cumulative_share_pct
FROM x
ORDER BY technical_failed_mn DESC;

-- 3) Priority quadrants
SELECT priority_quadrant, COUNT(*) AS banks,
       ROUND(SUM(total_volume_mn),2) AS volume_mn,
       ROUND(SUM(technical_failed_mn),2) AS technical_failed_mn
FROM bank_reliability
GROUP BY priority_quadrant
ORDER BY technical_failed_mn DESC;

-- 4) Reversal-quality exposure
SELECT bank_name, debit_reversal_count_mn, debit_reversal_success_pct,
       unresolved_reversal_mn
FROM bank_reliability
ORDER BY unresolved_reversal_mn DESC;

-- 5) Payer vs payee weighted reliability
SELECT side,
       ROUND(SUM(total_volume_mn),2) AS volume_mn,
       ROUND(100.0*SUM(technical_failed_mn)/SUM(total_volume_mn),3) AS weighted_td_pct,
       ROUND(100.0*SUM(business_failed_mn)/SUM(total_volume_mn),3) AS weighted_bd_pct
FROM psp_performance
GROUP BY side;

-- 6) UPI macro trend with window functions
SELECT month, banks_live, volume_mn, value_cr, avg_txn_value_inr,
       ROUND(100.0*(volume_mn/LAG(volume_mn) OVER(ORDER BY month)-1),2) AS volume_mom_pct_sql,
       ROUND(AVG(volume_mn) OVER(
         ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ),2) AS rolling_3m_volume_mn
FROM upi_macro
ORDER BY month;
