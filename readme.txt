Run a live database validation for the Helpline business-review changes in "behavioural_features_business_review.sql".

Use the existing SQL Server connection pattern already implemented in "sample.py".

Important:

- Reuse the existing connection code from "sample.py".
- Do not expose or print passwords, secrets, connection strings or tokens.
- Do not modify production/source data.
- Execute SELECT-only validation queries.
- Do not change the SQL feature logic yet.
- Use the same "@AsOfDate" and 12-month feature window currently defined in the standalone SQL.

Validate the following against the live database:

1. Feature coverage
   Return the number of distinct accounts where:

- "resolved_helpline_count_12m > 0"
- "super_to_pension_ttr_inquiry_count_12m > 0"
- "retirement_inquiry_count_12m > 0"
- "rollover_consolidation_inquiry_count_12m > 0"

Also return the corresponding 90-day feature coverage.

2. Raw examples
   For each new bucket return up to 20 actual source records showing:

- accountID
- call/event date
- outcomeDescription
- inquiryDescription
- derived bucket

3. Distinct source wording
   Return distinct matching descriptions and counts for:

- Resolved
- Super to Pension
- TTR
- Retirement
- Roll out
- Choice
- Consolidat

Show:

- description
- record count
- distinct account count

4. Overlap validation
   Do not rely only on the CASE-derived single bucket.

Evaluate each matching rule independently and identify source records that satisfy more than one rule.

Show:

- accountID
- date
- outcomeDescription
- inquiryDescription
- resolved_flag
- super_to_pension_ttr_flag
- retirement_flag
- rollover_consolidation_flag
- number_of_matching_buckets

5. Rollover / consolidation review
   Specifically check whether any records matched by:

- "Roll out"
- "Choice"
- "Consolidat"

appear to represent:

- consolidation inbound
- transfer into the fund
- general choice/product information
- any other non-exit intent

Show the distinct raw descriptions so they can be reviewed manually.

6. Super-to-Pension vs Retirement
   Show actual records where both:

- Super-to-Pension/TTR rule
  and
- Retirement rule

would match.

This is needed to determine whether the two concepts should remain separate.

7. Date integrity
   Confirm:

- no source record used is after "@AsOfDate"
- all records fall within the configured 12-month feature window

8. Account grain
   Execute the Helpline aggregate and confirm:

- total row count
- distinct accountID count
- duplicate accountID count

Expected duplicate accountID count = 0.

9. "helpline_active_days_12m"
   Confirm it is no longer in the active Helpline SELECT output and is retained only as a commented business-review candidate for removal.

Do not make any SQL changes based on the results yet.

At the end provide a table:

Check | Result | Status | Recommendation

Use:

- PASS
- REVIEW
- FAIL

Also clearly state whether Step 2 is safe to proceed as-is or whether the Helpline matching rules need adjustment before moving to the Campaign/Event block.
