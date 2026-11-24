Review and correct the exit type filtering logic in "target.py".

The source column "exitType" contains only three possible values:

- "Exit"
- "Internal Transfer"
- "NULL"

Update the target churn logic accordingly.

- Consider "Exit" within the defined outcome window as churn, subject to the existing business exclusion rules.
- Exclude internal transfers and deceased members as per the existing logic.
- Handle NULL values appropriately.
- Remove incorrect or unsupported exit type values from the filter conditions.
- Preserve the existing feature window, outcome window, eligibility rules and account-level modelling grain (one row per account_id per as_of_date).
- Do not modify any unrelated business logic or feature engineering.

Review the dependent files to identify whether the same incorrect filter is applied elsewhere. Restrict changes to "target.py" wherever possible. If changes are required in other files, report them with justification before modifying them.

Provide a summary of the changes and the SQL validation queries to verify the corrected churn counts.
