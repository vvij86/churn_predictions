Please identify candidate churn-prediction features from the MercerEdge tactical source and create a simple Excel workbook that can be understood by both technical and business users.

IMPORTANT:
This task is FEATURE IDENTIFICATION ONLY.

Do NOT perform feature engineering.
Do NOT write feature-generation SQL.
Do NOT modify build_merceredge_base_historical_dataset.sql.
Do NOT train any model.

Business has confirmed that:
edgePortalSource.pensionerData
is NOT required.

Exclude pensionerData completely.

Review these 17 in-scope tables:

1. merceredge.edgeSource.accountSummary
2. merceredge.edgeSource.accountEngagementWorkflow
3. merceredge.edgeSource.accountEngagementHelpline
4. merceredge.edgeSource.accountEngagementWeb
5. merceredge.edgeSource.AccountInsuranceCurrent
6. merceredge.edgeSource.accountInvestments
7. merceredge.edgeSource.accountMoneyInflow
8. merceredge.edgeSource.accountNetMoneyFlow
9. merceredge.edgeSource.accountRolloverPayment
10. merceredge.edgeSource.campaignEventDetails
11. merceredge.edgeSource.campaignEvents
12. merceredge.edgeSource.customerMapping
13. merceredge.edgeSource.customerSummary
14. merceredge.edgeSource.thirdPartyAuthority
15. merceredge.tableau.fundListSource
16. merceredge.edgeSource.campaign
17. merceredge.edgeSource.campaignAccountMapping

Use these files as source references:

- All_table_scripts.sql
- All_Other_tables_Not_explored.sql
- MercerEdge_ML_Churn_Driver_EDA_Phase2.xlsx
- MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables_part2.xlsx
- build_merceredge_base_historical_dataset.sql
- historical_snapshot_profile_results.json

Use actual table and column names from the DDL/EDA.
Do not guess.

Create an Excel file named:

MercerEdge_Churn_Candidate_Feature_List.xlsx

The Excel should be simple and business-friendly.

Sheet 1: Candidate_Features

Use these columns:

1. Feature Name
2. Simple Business Meaning
3. Feature Category
4. Source Table
5. Source Column(s)
6. Source Reference / File
7. Why It May Help Predict Churn
8. Behavioural Feature? Yes/No
9. Safe Before AsOfDate? Yes/No
10. Leakage Risk - Low/Medium/High
11. Business Confirmation Needed? Yes/No
12. Priority - High/Medium/Low
13. Recommendation - Use / Consider / Exclude

Keep the wording simple.

Examples of Simple Business Meaning:

- days_since_last_helpline_contact
  → "How long since the member last contacted the helpline"

- campaign_open_count
  → "How many campaign emails the member opened"

- contribution_count
  → "How often money was added to the account"

- negative_net_flow_count
  → "How often more money left the account than came in"

- partial_rollover_count
  → "How many times part of the member's money was rolled out"

Do not use highly technical descriptions unless necessary.

FEATURE GROUPS TO REVIEW

A. Behavioural / Engagement
- helpline activity
- web activity
- workflow activity
- campaign engagement
- member interaction/event activity
- recency/frequency of interactions

B. Transaction / Financial Behaviour
- money inflow
- contribution behaviour
- net money flow
- withdrawal/payment behaviour
- declining inflow
- negative cashflow

C. Rollover / Transfer Behaviour
- rollover activity
- partial rollover
- external rollover
- transfer activity

D. Investment Behaviour
- investment activity
- investment changes
- investment holding/value where historically safe

E. Insurance
- active insurance
- cover/premium
- insurance status

F. Account / Tenure / Product
- tenure
- member/account type
- fund/product information
- member source

G. Campaign / Communication
- campaigns sent
- opens
- clicks
- engagement rate
- time since last interaction

IMPORTANT LEAKAGE RULE

Do not recommend future/outcome information as predictive features.

Clearly mark as EXCLUDE where applicable:

- exitDate
- MEMBER_EXIT
- account closure outcome
- full rollover completion when it represents the churn event
- future payment/rollover activity after @AsOfDate
- any field that directly reveals future churn

Sheet 2: Top_Features

Create two simple sections:

A. Top 10 Behavioural Features
B. Top 10 Overall Churn Features

For each include:

- Rank
- Feature Name
- Simple Meaning
- Source Table
- Source Column(s)
- Why Important

Sheet 3: Excluded_Leakage_Features

Include:

- Field/Event
- Source Table
- Source Column
- Reason for Exclusion
- Leakage Explanation in Simple Terms

Example:
MEMBER_EXIT
Reason:
"Shows that the member has already exited, so the model would be learning the answer instead of predicting it."

Sheet 4: Business_Confirmation

List only features/events where business clarification is still required.

Columns:

- Feature/Event
- Source
- Question for Business
- Why Confirmation Is Needed

Sheet 5: Table_Summary

For all 17 tables show:

- Table Name
- Main Business Purpose
- Useful for Churn? Yes/Maybe/No
- Main Candidate Feature Types
- Behavioural Value - High/Medium/Low
- Comments

IMPORTANT:
The Excel should be concise, clean and easy to review in a meeting.

Use short sentences.
Avoid ML jargon where possible.

Do not calculate the features.
Do not create SQL.
Only identify and document candidate features with clear source references.

At the end, show me:
- total number of candidate features identified
- number of behavioural features
- number marked High priority
- number excluded due to leakage
- Excel file location
