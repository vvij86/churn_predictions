For FR-ML-017, your lead is right: because the Business Confirmation Status is already “Confirmed”, the requirement should not say “may be used.” It should state clearly that website engagement is in scope.

I’d change FR-ML-017 to:

Requirement / Description:
Website engagement

Business Rule / Current Position:

> Website engagement is included as a behavioural feature group for churn prediction. Features include website activity count and days since last website activity. accountEngagementWeb is not populated in UAT, therefore these features will be validated using the Prod/Databricks source.



Example:

> Website activities in previous 12 months = 8; days since last website activity = 15.



Business Confirmation Status:

> Confirmed



Comments / Open Points:

> UAT source is not populated; feature validation to be completed using Prod/Databricks data.



That is much cleaner because it separates two things:

> Business decision: Website engagement will be used.
Technical limitation: UAT currently has no data, so the feature values still need Prod validation.



I would also review the rest of your FRS for words like “may,” “could,” “possibly,” “where available,” etc. For a row marked Confirmed, use firm wording such as “is included,” “will be used,” “is excluded,” “must be,” etc.

For rows still marked Open, softer wording is fine because the decision has not yet been made.
