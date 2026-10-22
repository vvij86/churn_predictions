I checked the transitioned-member exit logic from the business SQL. To reproduce the exact rule, it is using the fund lookup ("MercerDM.span.fundList") to derive the sub-fund, along with accountSummary fields.

Just wanted to confirm — will the FundScope/database filtering and transitioned-member exclusion already be applied before the data reaches the Databricks views, or should we handle these filters within the ML feature/eligibility logic?
