Update only the Helpline feature section in "behavioural_features_business_review.sql".

Do not modify Campaign/Event, Workflow, Website, Contribution, Rollover, Investment, Insurance, Third Party Authority, Net Money Flow, Account/Tenure/Product or any other section.

Implement the following business-review changes.

1. Add a "RESOLVED" helpline bucket where:

"outcomeDescription LIKE '%Resolved%'"

Create:

- "resolved_helpline_count_12m"
- "recent_resolved_helpline_count_90d"

2. Add a "SUPER_TO_PENSION_TTR" bucket where either "outcomeDescription" or "inquiryDescription" contains:

- "Super to Pension"
- "TTR"

Create:

- "super_to_pension_ttr_inquiry_count_12m"
- "recent_super_to_pension_ttr_inquiry_count_90d"

3. Add a "RETIREMENT_INQUIRY" bucket where "outcomeDescription" or "inquiryDescription" contains:

"Retirement"

Create:

- "retirement_inquiry_count_12m"
- "recent_retirement_inquiry_count_90d"

4. Add a "ROLLOVER_CONSOLIDATION_INTENT" bucket where "inquiryDescription" contains any of:

- "Roll out"
- "Choice"
- "Consolidat"

Create:

- "rollover_consolidation_inquiry_count_12m"
- "recent_rollover_consolidation_inquiry_count_90d"

Where possible, exclude inbound consolidation activity so that consolidation INTO the fund is not interpreted as potential exit intent.

5. Business questioned the usefulness of:

"helpline_active_days_12m"

Do not permanently delete it yet. Comment it out or clearly mark it:

"-- BUSINESS REVIEW: candidate for removal - generic active days considered low value"

6. Do not modify the existing complaint features in this step. Business has raised concerns about complaint source coverage, but we will review that separately.

7. All source records used for these features must:

- be on or before "@AsOfDate"
- remain within the existing 12-month feature window
- use no future/outcome-period information

8. Preserve account-level aggregation:
   one row per "accountID".

9. Do not change eligibility or target logic.

10. Add the comment:

"-- BUSINESS REVIEW CHANGE"

around every new or changed Helpline section.

After making the changes, append validation SQL that shows:

A. Number of accounts where each new feature is > 0.

B. Top 20 sample accounts for:

- Resolved
- Super-to-Pension/TTR
- Retirement
- Rollover/Consolidation

C. For those samples, show the raw:

- "accountID"
- event/contact date
- "outcomeDescription"
- "inquiryDescription"
- derived bucket

D. Check whether any source record used has a date greater than "@AsOfDate".

E. Check for duplicate "accountID" rows in the final Helpline aggregation.

Do not change any SQL outside the Helpline feature block.

After completing the changes, summarize exactly:

- features added
- feature commented/de-scoped
- any overlap observed between buckets
- any issue requiring business confirmation
