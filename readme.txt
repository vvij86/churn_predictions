Update only the Helpline section in "behavioural_features_business_review.sql".

Do not modify Campaign/Event, Workflow, Website, Contribution, Rollover, Investment, Insurance, Third Party Authority, Net Money Flow, Account/Tenure/Product, eligibility logic, target logic, or any other section.

We completed live source-data validation and need the following corrections.

1. Keep the existing RESOLVED logic as-is.

The live values confirmed that:

"outcomeDescription LIKE '%Resolved%'"

correctly captures values such as:

- Inquiry Resolved with Admin Assistance
- Email inquiry resolved by Helpline services
- Inquiries Resolved by Helpline Services

Keep these features:

- "resolved_helpline_count_12m"
- "recent_resolved_helpline_count_90d"

2. Modify SUPER_TO_PENSION_TTR logic.

The live data showed that "outcomeDescription = 'Super to Pension Implementation'" is a strong transition signal and appears across many different inquiry types.

Use an independent flag/bucket for Super-to-Pension/TTR based on:

- "outcomeDescription LIKE '%Super to Pension%'"
- OR "outcomeDescription LIKE '%TTR%'"
- OR "inquiryDescription LIKE '%TTR%'"

Do not require "inquiryDescription" to contain "Super to Pension".

Keep/create:

- "super_to_pension_ttr_inquiry_count_12m"
- "recent_super_to_pension_ttr_inquiry_count_90d"

3. Modify RETIREMENT_INQUIRY logic.

The live data showed clear retirement inquiry values such as:

- Retirement / Pension
- Retirement Optimiser
- Retirement planning

Therefore derive Retirement Inquiry primarily from:

"inquiryDescription LIKE '%Retirement%'"

Do not use "outcomeDescription LIKE '%Retirement%'" for this feature unless the existing data proves that is required.

Keep/create:

- "retirement_inquiry_count_12m"
- "recent_retirement_inquiry_count_90d"

4. Important: Super-to-Pension/TTR and Retirement Inquiry must be independent features.

Do not force these concepts into a single mutually-exclusive CASE bucket.

A single source record may legitimately satisfy both.

Example:

"outcomeDescription = 'Super to Pension Implementation'"
"inquiryDescription = 'Retirement / Pension'"

This should contribute to:

- Super-to-Pension/TTR feature
  AND
- Retirement Inquiry feature

This overlap is intentional because the two features represent different concepts:

- Retirement Inquiry = retirement intent / enquiry
- Super-to-Pension/TTR = stronger transition-to-pension behaviour

5. Do not change the RESOLVED feature because a resolved call may also be a retirement-related call.

Resolved represents service outcome.
Retirement represents inquiry intent.

They can coexist as separate signals.

6. Keep the current date rules:

- source date >= existing FeatureStartDate
- source date <= "@AsOfDate"
- preserve the 12-month feature window
- preserve recent 90-day logic

7. Preserve account-level grain:
   one row per "accountID".

8. Keep "helpline_active_days_12m" commented/de-scoped as already implemented.

9. Do not modify the ROLLOVER_CONSOLIDATION_INTENT logic in this change.
   We will update that separately after reviewing Point 4.

10. Add:
    "-- BUSINESS REVIEW CHANGE - LIVE DATA VALIDATED"
    around the modified Super-to-Pension/TTR and Retirement Inquiry logic.

After making the change, validate:

- number of accounts with Super-to-Pension/TTR > 0
- number of accounts with Retirement Inquiry > 0
- number of accounts having both features > 0
- top 20 raw records for Super-to-Pension/TTR
- top 20 raw records for Retirement Inquiry
- top 20 records where both features match
- duplicate accountID count in final Helpline aggregation
- confirm no source record used is after "@AsOfDate"

Do not modify any unrelated SQL.

At the end summarize:

- exact logic changed
- features retained
- overlap count between Retirement and Super-to-Pension/TTR
- whether validation passed
