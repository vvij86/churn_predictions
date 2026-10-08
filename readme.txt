Please create a separate SQL validation file for the candidate churn features identified from the 17 in-scope MercerEdge tables.

IMPORTANT:
This is FEATURE VALIDATION ONLY.

Do NOT perform feature engineering.
Do NOT build aggregate ML features.
Do NOT modify build_merceredge_base_historical_dataset.sql.
Do NOT train any model.

Exclude:
edgePortalSource.pensionerData

Create a new file:

validate_candidate_churn_features.sql

Purpose:
Provide simple read-only SQL checks that I can run manually to validate whether the identified candidate churn features have useful data.

For each relevant source table/column, add small profiling queries such as:

1. Row count
2. Distinct accountID count
3. NULL count / NULL percentage
4. Distinct values for categorical columns
5. MIN/MAX dates for date columns
6. MIN/MAX/AVG for numeric columns where useful
7. TOP sample rows
8. Multiple rows per account check for behavioural/event tables
9. Date coverage relative to the modelling period
10. Simple checks for target leakage / future information

Focus especially on behavioural features from:

- accountEngagementWorkflow
- accountEngagementHelpline
- accountEngagementWeb
- accountMoneyInflow
- accountNetMoneyFlow
- accountRolloverPayment
- campaignEventDetails
- campaignEvents
- campaignAccountMapping
- accountInvestments
- AccountInsuranceCurrent

Also include supporting checks for:

- accountSummary
- customerMapping
- customerSummary
- thirdPartyAuthority
- fundListSource
- campaign

Keep each query simple and clearly commented.

Example format:

--------------------------------------------------
-- Feature candidate: Helpline contact frequency
-- Business meaning: How often the member contacts the helpline
-- Source: edgeSource.accountEngagementHelpline
-- Columns: accountID, callDate
--------------------------------------------------

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT accountID) AS distinct_accounts,
    MIN(callDate) AS min_call_date,
    MAX(callDate) AS max_call_date,
    SUM(CASE WHEN callDate IS NULL THEN 1 ELSE 0 END) AS null_call_dates
FROM merceredge.edgeSource.accountEngagementHelpline;

Then add a small sample query if useful.

Do the same for each important candidate feature source.

Do NOT create features such as:
- helpline_contact_count_12m
- campaign_open_rate
- negative_net_flow_count
- rollover_count

Only validate the raw columns needed to create those features later.

At the top of the SQL file, add a short comment explaining:

"These queries validate candidate feature sources only. They do not perform feature engineering."

At the end, include a compact summary comment listing:
- feature area
- source table
- main source columns
- what the query validates

Use actual column names from the DDL files.
Do not guess column names.
Use read-only SQL only.
