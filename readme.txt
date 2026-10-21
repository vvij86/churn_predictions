Use this Copilot prompt:

> Read member_retention_ml_copilot_instructions.md first.

Review the current behavioural_features_business_review.sql and identify all behavioural features that have been defined so far.

Also use the supporting reference files only where needed to confirm the source/meaning:

- MemberRetention_01-AccountBase_v006.sql
- MemberRetention_03-MemberRetentionMetrics_v005.sql
- MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
- MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
- All_table_scripts.sql
- All_Other_tables_Not_explored.sql

Create a new Word document:

Member_Retention_Behavioural_Feature_List.docx

Do not modify any existing Word document.

Objective

Create a simple business-friendly document listing only the behavioural features identified so far.

This document is for business/team review, so keep the descriptions very high level and easy to understand by a non-technical person.

Do not include SQL code.

Do not include model-development details.

Do not include target/churn label fields.

Do not include account/tenure/product fields unless they are genuinely behavioural.

Document structure

Add a short title:

Member Retention ML – Behavioural Feature List

Under the title, add one short sentence:

This document lists the behavioural features identified for the Member Retention ML model for business review and confirmation.

Then create one table with these columns:

1. S.No
2. Behaviour Name
3. Behaviour Type
4. Description
5. Sample Value
6. Source
7. Comments

Column guidance

S.No

Sequential numbering starting from 1.

Behaviour Name

Use a clean business-friendly name rather than only the technical SQL column name.

Example:

Helpline Contact Count - 12 Months

instead of:

helpline_contact_count_12m

Behaviour Type

Use simple categories such as:

- Helpline Engagement
- Website Engagement
- Workflow Activity
- Contribution Behaviour
- Money Flow Behaviour
- Rollover / Withdrawal Behaviour
- Investment Behaviour
- Insurance Behaviour
- Third Party Authority
- Campaign / Event Behaviour
- Customer Experience / Qualtrics

Use only categories actually represented in the current feature list.

Description

Write one short sentence in plain English.

Keep it understandable to a layman.

Examples:

- Number of times the member contacted the helpline during the last 12 months.
- Number of days since the member last contacted the helpline.
- Shows whether the member’s contribution activity has reduced recently.
- Number of partial rollover transactions made during the last 12 months.

Avoid technical terms such as:

- aggregation
- CTE
- point-in-time
- lag
- window function
- feature engineering

unless absolutely necessary.

Sample Value

Give a simple illustrative value based on the feature type.

Examples:

- 5
- 109 days
- ₹1,500
- Yes / No
- 3 months
- 2 events

Do not claim sample values are actual production values unless they are directly supported by the SQL output.

If using illustrative values, keep them clearly generic.

Source

Mention the main source table only.

Examples:

- edgeSource.accountEngagementHelpline
- edgeSource.accountEngagementWorkflow
- edgeSource.accountMoneyInflow
- edgeSource.accountNetMoneyFlow
- edgeSource.accountRolloverPayment
- edgeSource.accountInvestments
- edgeSource.AccountInsuranceCurrent
- edgeSource.thirdPartyAuthority
- edgeSource.campaignEventDetails / campaignEvents

Where a feature is derived from more than one source, list both briefly.

Comments

Leave this column blank for business comments.

Do not pre-populate comments.

Scope rules

Include only behavioural features already identified in behavioural_features_business_review.sql.

Include:

- helpline features
- website features
- workflow features
- contribution features
- money-flow features
- rollover / withdrawal features
- investment-related behavioural features
- insurance-related behavioural features if currently included
- third-party-authority behavioural indicator if currently included
- campaign/event behavioural features from campaignEventDetails and campaignEvents if they are currently included

Important campaign scope:

- campaignEventDetails and campaignEvents are in scope
- campaign and campaignAccountMapping are deferred and should not be listed as active behavioural features

Do not include:

- target_churn
- churn outcome fields
- exitDateRecorded
- MEMBER_EXIT
- eligibility flags
- fund-scope fields
- technical validation fields
- duplicate-count fields
- model metrics
- account identifiers

If a candidate feature is still marked REVIEW REQUIRED, it can still be listed, because this document is for business review. Do not remove it just because confirmation is pending.

For website features, if UAT is not populated, still include the feature in the list, because it remains in scope for Prod/Databricks validation.

Formatting

- Use a clean professional Word table.
- Make the header row bold.
- Keep descriptions short.
- Use readable column widths.
- Do not use excessive colours or graphics.
- Keep the document easy to print and review.
- Use landscape orientation if needed to fit all columns cleanly.

Validation before finishing

Confirm that:

- every behavioural feature currently defined in behavioural_features_business_review.sql is represented once
- there are no duplicate features
- no target/outcome fields are included
- descriptions are business-friendly
- the Comments column is completely blank
- sources match the SQL/reference files

Save the final output as:

Member_Retention_Behavioural_Feature_List.docx

Stop after creating the Word document.
