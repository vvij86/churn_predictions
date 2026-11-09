
Review "behavioural_features_business_review.sql" only.

Do not modify any SQL yet.

I want you to understand and document the existing structure before we make business-review changes.

Please do the following:

1. Identify each existing feature block, including:
   
   - Helpline
   - Campaign / Event
   - Website
   - Workflow
   - Contribution / Money Inflow
   - Partial Rollover / Withdrawal
   - Investment
   - Insurance
   - Third Party Authority
   - Net Money Flow

2. For each feature block, list:
   
   - source table(s)
   - feature names currently generated
   - lookback period used, such as 12 months, 90 days, 30 days or as-of
   - aggregation grain

3. Confirm whether every aggregated feature block returns one row per "accountID".

4. Identify features that appear to be logically duplicated across different sources. For example:
   
   - Advice from Helpline vs Campaign/Event
   - Contribution from Campaign/Event vs "accountMoneyInflow"
   - Roll-in / rollover signals from Campaign/Event vs payment/rollover tables
   - Member service activity across Helpline, Campaign and Workflow

5. Identify any existing features that may create target leakage, especially anything related to:
   
   - member exit
   - full rollover
   - external payment
   - account closure
   - events occurring after "@AsOfDate"

6. Confirm that source records used for predictors are filtered to dates on or before "@AsOfDate".

7. Identify generic features that may be difficult for business users to interpret, such as generic event counts or activity-day counts.

8. Do not suggest new SQL yet and do not change the file.

At the end, give me a concise summary in this format:

- Feature block
- Source table
- Existing features
- Possible duplication
- Possible leakage concern
- Business interpretability concern
- Any issue requiring review

Keep the analysis specific to the current SQL file.
