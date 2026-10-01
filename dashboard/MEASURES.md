# Suggested Power BI Measures

```DAX
Total Volume Mn = SUM(BankReliability[total_volume_mn])
Technical Failures Mn = SUM(BankReliability[technical_failed_mn])
Business Failures Mn = SUM(BankReliability[business_failed_mn])
Weighted TD % = DIVIDE([Technical Failures Mn], [Total Volume Mn])
Weighted BD % = DIVIDE([Business Failures Mn], [Total Volume Mn])
Approved Volume Mn = SUM(BankReliability[approved_volume_mn])
Unresolved Reversals Mn = SUM(BankReliability[unresolved_reversal_mn])
Banks Above 1% TD = CALCULATE(DISTINCTCOUNT(BankReliability[bank_name]), BankReliability[technical_decline_pct] >= 1)
```
