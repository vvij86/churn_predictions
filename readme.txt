Validate the attached Word document against "behavioural_features_business_review.sql".

The SQL file is the source of truth.

For each standalone query:

- identify only the columns returned in the final "SELECT"
- exclude SQL syntax, functions, parameters, helper columns and intermediate expressions
- do not include values such as "(", "DAY", "@AsOfDate", CASE expressions, CTE fields, accountID or AsOfDate unless they are actual intended behavioural features

Check every row in the Word document against the corresponding final SQL output.

Fix any incorrect, missing or extra rows.

For each valid feature, ensure:

- Behaviour Name = exact final SQL feature alias
- Description = simple business-friendly meaning
- Sample Value = realistic example
- Source = actual source table/view used by that feature
- Comments = blank

Keep the current document structure:

- separate table for each behaviour group
- columns:
  "S.No | Behaviour Name | Description | Sample Value | Source | Comments"

Do not add a Behaviour Type column.

Do not invent any feature.

Before saving the corrected Word file, perform a final validation that every row in every table maps to a real final "SELECT" feature in the SQL.
