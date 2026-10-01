# Limitations

1. **Aggregate, not transaction-level.** No user-level attempts, retry chains, merchant IDs or detailed response codes are available in the packaged dataset.
2. **Different source dates.** Bank/PSP analysis is an Aug 2025 snapshot; macro product trend is Apr–Aug 2026. The project does not pretend they are the same reporting period.
3. **Derived failure counts.** `volume × TD%` is an estimate from published aggregate metrics.
4. **No revenue-recovery claim.** Public data does not show whether a failure was retried and later completed.
5. **System-wide ticket size.** Average transaction value is not bank-specific.
6. **Snapshot coverage.** The packaged bank table is a compact subset of the published top-member table, not every UPI participant.
7. **Benchmark wording.** The 1% TD line is used as an analytical benchmark; verify any current regulatory/compliance interpretation before using it externally.
8. **No causal inference.** A high decline rate does not identify the underlying technical cause.
