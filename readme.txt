Using the validated standalone feature queries in "behavioural_features_business_review.sql", prepare a consolidated feature dataset SQL query for review/readiness purposes only.

This is not the start of model development or production implementation.

The purpose is to have a review-ready SQL that shows how the approved standalone feature groups can be combined into one account-level feature dataset.

Requirements:

- Grain: one row per "accountID + @AsOfDate"
- Reuse the existing validated standalone feature logic without redesigning it
- Use the eligible account population from "accountSummary" as the base
- Combine these groups:
  - Account / Tenure / Product
  - Helpline
  - Website
  - Workflow
  - Campaign / Event
  - Contribution
  - Partial Rollover
  - Investment / FUM
  - Insurance
  - Third Party Authority
  - Net Money Flow
- Preserve existing AsOfDate, point-in-time and leakage rules
- Keep "current_account_fum_amount" from the validated accountInvestments as-of logic
- Do not add "target_churn"
- Do not add model training, validation, scoring, MLOps or deployment logic
- Do not overwrite the standalone query file

Create a new SQL file containing the consolidated feature dataset query so it is ready for technical/business review before development starts.
