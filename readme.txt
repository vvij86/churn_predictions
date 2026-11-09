Review only the ADVICE and COMPLAINT logic in the Helpline section of "behavioural_features_business_review.sql".

Do not modify SQL yet.

For ADVICE:

Current values include:

- SOA
- Projection advice
- Financial Advice
- Financial Adviser Contact
- MST workplace advice
- Retirement planning
- TTR advice

Using live source data, return for each value:

- record count
- distinct account count
- earliest callDate
- latest callDate
- count within the current 12-month feature window
- top 10 raw examples with accountID, callDate, outcomeDescription, inquiryDescription

Also identify overlap with:

- "RETIREMENT_INQUIRY"
- "SUPER_TO_PENSION_TTR"

Specifically check whether "Retirement planning" and "TTR advice" are already being captured by those independent business-reviewed features.

Recommend for each advice value:
KEEP / REVIEW / REMOVE FROM ADVICE BUCKET

Do not remove anything yet.

For COMPLAINT:

Validate:

- total complaint records
- distinct accounts
- coverage in current 12-month window
- 90-day coverage
- 30-day coverage
- top 20 raw records

Also state clearly that business commented that Helpline complaints may represent only a subset of all complaints and another source/workbook may provide broader complaint coverage.

Do not assume Helpline complaints are complete.

At the end provide:

Feature | Current logic | Live coverage | Overlap concern | Business concern | Recommendation

Do not modify any SQL in this step.
