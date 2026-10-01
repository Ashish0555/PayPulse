# Power BI Model

Recommended relationships:
- `dim_bank[bank_key]` 1 → * `fact_bank_reliability[bank_key]`
- `dim_date[month]` 1 → * `fact_bank_reliability[month]`
- `dim_date[month]` 1 → * `upi_macro_2026_enriched[month]`

The payer/payee PSP tables are intentionally kept as a separate analytical table because PSP entities are not identical to remitter-member bank entities.
