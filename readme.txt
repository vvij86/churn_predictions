Validate only the Helpline changes you just added in "behavioural_features_business_review.sql".

Do not modify the SQL yet.

Please run/review the validation logic and report the results for:

1. New feature coverage:
   
   - number of accounts with "resolved_helpline_count_12m > 0"
   - number of accounts with "super_to_pension_ttr_inquiry_count_12m > 0"
   - number of accounts with "retirement_inquiry_count_12m > 0"
   - number of accounts with "rollover_consolidation_inquiry_count_12m > 0"

2. Show up to 20 raw source examples for each new bucket, including:
   
   - accountID
   - source event/contact date
   - outcomeDescription
   - inquiryDescription
   - derived bucket

3. Check overlap:
   
   - identify any raw record matching more than one new bucket
   - show the overlapping bucket names and raw description text

4. Specifically review "ROLLOVER_CONSOLIDATION_INTENT" and show the distinct matching "inquiryDescription" values.
   Confirm whether any appear to represent inbound consolidation or other non-exit intent.

5. Specifically review "SUPER_TO_PENSION_TTR" and "RETIREMENT_INQUIRY".
   Show whether the same descriptions are being captured by both buckets.

6. Validate date integrity:
   
   - confirm no source record used by these features is after "@AsOfDate"
   - confirm the existing 12-month feature window is respected

7. Validate account-level grain:
   
   - confirm the final Helpline aggregate has no duplicate "accountID"

8. Confirm "helpline_active_days_12m" is no longer part of the active output and is only retained/commented as a business-review candidate for removal.

9. Do not make fixes automatically.

At the end, provide a short PASS / REVIEW / FAIL summary for each check and list any SQL changes you recommend before we proceed to the next feature block.
