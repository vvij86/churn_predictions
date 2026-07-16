The proposed dataset specification is useful.

For Version 1 of my POC, I want to use SonataODS only.
Salesforce will be added later as Version 2.

Please revise the specification with the following rules:

1. Remove all Salesforce tables, columns and join requirements.
2. Keep the dataset grain as one row per account_id.
3. account_id is the mandatory identifier.
4. client_id may be retained only as an optional reference field and must
   not be used as an ML feature.
5. target_churn = 0 based on FR-RR-006 retained rules.
6. target_churn = 1 based on FR-RR-007 not-retained rules.
7. Death-related exits must be excluded.
8. Partial rollover may be retained as a historical risk feature.
9. Full rollover out, account closure due to full exit, exit date,
   exit reason and post-exit account status must be target-supporting
   fields only and must not be model features.
10. All feature values must be calculated using data available on or before
    the as_of_date.
11. Do not generate SQL or Python code yet.

Please provide:

A. A revised SonataODS-only final dataset structure.
B. For every proposed column, show:
   - proposed final column name
   - source table
   - source column or calculation
   - identifier / feature / target-supporting / exclusion / target category
   - historical time window required
   - possible leakage risk
C. Clearly mark any proposed feature whose source or business meaning
   cannot be confirmed from the available SonataODS scripts.
D. List only the remaining information I need to confirm before SQL can
   be generated.
