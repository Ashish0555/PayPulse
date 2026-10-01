# Interview Prep — PayPulse

## 30-second explanation
“I built PayPulse to test a common operations-analytics problem: percentages can hide scale. Using official NPCI UPI reliability statistics, I derived estimated technical-failure counts, compared TD-rate rank with absolute-impact rank, built a Pareto view, analyzed reversal quality and packaged the model into SQL, Excel and Power BI-ready tables. I deliberately kept the claims aggregate and did not invent transaction-level revenue impact.”

## Questions to prepare for
**Why separate BD and TD?** NPCI defines BD as non-technical/business declines and TD as technical/system/network-related declines. They imply different remediation paths.

**Why can TD% be misleading?** A low percentage on massive volume can create more failed attempts than a high percentage on a small institution.

**Why multiply volume by TD%?** It converts the published rate into an estimated failure count for prioritization. I label it derived because row-level failures are unavailable.

**Why not calculate “lost revenue”?** Retry outcome and merchant-specific ticket size are not observable in this dataset.

**Why SQLite?** It keeps the project reproducible and interview-friendly while still demonstrating relational modeling and advanced SQL.

**What would you request in production?** Monthly bank panels, response codes, retry IDs, latency, merchant segment and final payment outcome.
