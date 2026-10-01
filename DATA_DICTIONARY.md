# Data Dictionary

## bank_reliability
| Field | Meaning |
|---|---|
| month | Observation month (`YYYY-MM`) |
| bank_name | NPCI remitter-member name |
| total_volume_mn | Published transaction volume, millions |
| approved_pct | Published approval percentage |
| business_decline_pct | Published Business Decline percentage |
| technical_decline_pct | Published Technical Decline percentage |
| debit_reversal_count_mn | Published debit reversal count, millions |
| debit_reversal_success_pct | Published debit reversal success percentage |
| technical_failed_mn | Derived: volume × TD% |
| business_failed_mn | Derived: volume × BD% |
| unresolved_reversal_mn | Derived: reversal count × (1 − reversal success%) |
| td_absolute_rank | Rank by derived technical-failure count |
| td_rate_rank | Rank by TD% |
| priority_quadrant | Rate × scale operational segment |

## psp_performance
Payer/payee PSP-side volumes and published Approved/BD/TD percentages, plus derived failure counts.

## upi_macro
Monthly UPI system volume, value, live-bank count, average transaction value and month-over-month change.
