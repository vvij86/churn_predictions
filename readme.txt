
Update only the Helpline section in "behavioural_features_business_review.sql".

Based on the completed live-data review:

1. ADVICE bucket:
   Keep only these values in the ADVICE category:

- SOA
- Projection advice
- Financial Advice
- Financial Adviser Contact
- MST workplace advice

Remove these values from the ADVICE category:

- Retirement planning
- TTR advice

Reason:

- "Retirement planning" is already captured by the independent "RETIREMENT_INQUIRY" feature.
- "TTR advice" is already captured by the independent "SUPER_TO_PENSION_TTR" feature.
- We do not want the same business behaviour represented twice as separate advice evidence.

Do not change the existing RETIREMENT_INQUIRY or SUPER_TO_PENSION_TTR logic.

2. COMPLAINT:
   The live validation found:

- 8 total complaint records
- 5 distinct accounts
- only 1 record in the current 12-month window
- 0 records in the 90-day window
- 0 records in the 30-day window

Business also commented that Helpline complaints represent only a subset of all complaints and broader complaint data may exist elsewhere.

Therefore de-scope these Helpline complaint features from the active output:

- complaint_inquiry_count_12m
- recent_complaint_inquiry_count_90d
- recent_complaint_flag_30d

Do not delete the logic permanently.

Comment the complaint classification/feature logic and add:

"-- BUSINESS REVIEW: de-scoped from active ML features because Helpline complaint coverage is sparse/incomplete; broader complaint source to be assessed separately."

3. Do not modify:

- resolved features
- Super-to-Pension/TTR features
- retirement inquiry features
- rollover/consolidation features
- other Helpline categories
- any other feature block

4. Run the live validation after the change and confirm:

- no duplicate accountID rows
- no source records after AsOfDate
- ADVICE no longer contains Retirement planning or TTR advice
- RETIREMENT_INQUIRY still captures Retirement planning
- SUPER_TO_PENSION_TTR still captures TTR advice
- complaint features are no longer present in the active Helpline output

Give me a short PASS/FAIL summary. Do not change any other SQL.
