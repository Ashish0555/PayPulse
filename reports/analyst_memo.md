# PayPulse — Analyst Memo

## Executive summary
This analysis is designed to support operational triage, not causal attribution. The key business question is straightforward: when failure rate and absolute failure burden disagree, which institutions deserve immediate operational attention?

The packaged August 2025 bank snapshot suggests that the answer is not a single “worst bank.” Instead, the portfolio splits into two distinct risk patterns:

- high-rate, high-impact institutions that need direct technical remediation
- large banks with moderate rate but material failure volumes that require scale-focused monitoring

## Main findings
- **Bank Of India** is the clearest high-priority institution. It combines the highest technical-decline rate in the sample and one of the largest derived failure volumes.
- **State Bank of India** illustrates the rate-vs-scale problem well. Its percentage is far lower than the worst performers, but its sheer transaction volume creates a material operational burden.
- The portfolio is concentrated: a small share of institutions generates a disproportionate portion of technical-failure burden, which is consistent with a Pareto-style reliability risk profile.
- Unresolved debit reversals are materially elevated for the same institutions that appear in the highest-risk segments, which strengthens the case for prioritizing root-cause investigation rather than simple monitoring.
- The system-level UPI macro trend remains healthy in aggregate, with volume and value continuing to expand through Aug 2026, even as operational stress remains concentrated in specific institutions.

## Operational interpretation
1. Use technical-decline percentage to identify institutions with structurally weak reliability.
2. Use absolute technical failures to identify institutions with the largest operational load.
3. Treat the intersection of both dimensions as the highest-priority remediation group.
4. Keep Business Declines separate from Technical Declines because they reflect different failure modes and operational fixes.
5. For monitoring and escalation, track the institutions that are not the worst on rate but are still large enough to create customer-impacting scale issues.

## Recommended prioritization
- **ACT_NOW**: institutions with both high technical-decline rate and above-median technical impact
- **WATCH_SCALE**: institutions with moderate rate but large absolute technical-failure impact
- **FIX_RATE**: institutions with elevated rate but smaller absolute burden
- **LOWER_PRIORITY**: institutions below both thresholds

This framework improves decision quality without overstating what the public data can support. It helps teams focus investigation where the risk is highest, while keeping the analysis grounded in aggregated, published figures.

## Data limitations
This model is useful for prioritization but not for definitive root-cause diagnosis. It does not include response-code detail, retry chains, attempt-level latency, merchant segmentation, or final settlement outcomes. These are the missing fields required for a production-grade technical investigation.

## Next step for a production version
To move from triage to action, the next iteration should add:
- multi-month bank panels
- response-code and failure-category data
- retry and retry-success detail
- API or network latency metrics
- PSP/merchant segment-level splits
- final outcome and resolution timing

That would allow the project to move from an analytical prioritization tool into a true operational reliability dashboard.
