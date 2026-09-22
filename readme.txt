Use this prompt in Copilot:

I have completed churn-focused data exploration for 85 MercerEdge tables and generated the workbook:

MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables.xlsx

Now I want you to identify the MOST IMPORTANT tables for churn / retention modelling.

Do not simply rank tables by number of columns. Assess them based on actual churn relevance.

Use the workbook contents, especially:
- Useful for Churn
- Decision
- Reason
- Feature Group
- Data Quality Notes
- Null %
- Date Coverage
- Leakage Risk
- Recommended Action
- Overview sheet

Also consider the business context:
- Modelling grain is account level
- Final grain will be one row per account_id + as_of_date
- Features should represent information available on or before as_of_date
- Avoid target leakage / future information
- IDs are mainly for joining/reference and are not predictive features
- We are trying to predict future account churn/retention

Identify tables that can provide meaningful churn drivers such as:
- contributions / money inflow
- withdrawals / money outflow
- rollovers
- account balance / FUM
- net money flow
- account tenure / lifecycle
- investment behaviour
- web engagement
- helpline / customer contact
- communication preferences
- insurance
- account/product characteristics
- behavioural changes / recency / frequency
- other strong behavioural indicators

Please classify all 85 tables into these groups:

1. High Priority – Strong candidate for churn feature engineering
2. Medium Priority – Potentially useful, but needs further validation/business clarification
3. Low Priority – Mainly reference/join/supporting data
4. Exclude – No meaningful churn value, unusable data, or mainly technical/audit data

For each High Priority table provide:

- Table Name
- Why it is important for churn
- Important candidate columns
- Potential feature group
- Example derived ML features
- Data quality concern
- Leakage concern
- Recommended next action

Example derived features could be:

- contribution_count_3m
- contribution_amount_12m
- months_since_last_contribution
- withdrawal_count_12m
- rollover_out_amount_12m
- net_money_flow_12m
- balance_change_3m
- web_activity_count_3m
- days_since_last_web_activity
- helpline_contact_count_6m
- investment_activity_count_12m

IMPORTANT:
- Be selective.
- Do not call a table High Priority only because it has one potentially useful column.
- Prefer tables with meaningful account-level behavioural, financial, lifecycle, or engagement information.
- Consider actual data quality and date coverage.
- Tables with 100% null / very sparse important columns should be downgraded appropriately.
- Tables containing outcome/future fields may still be useful for target creation, but clearly mark them as TARGET-SUPPORT / LEAKAGE RISK rather than predictive feature tables.
- Do not use identifiers alone as a reason to rank a table highly.
- Avoid duplicate tables providing essentially the same information; explain which one should be preferred.

At the end, give me:

1. Top 10 most important tables for churn modelling
2. Next 10 tables worth investigating
3. Tables mainly useful for target creation / churn-event identification
4. Tables mainly useful only for joins/reference
5. Tables that can safely be excluded from further ML exploration

For the Top 10, provide a short final summary in this format:

Table Name | Priority | Main Churn Signal | Key Candidate Columns | Example Features | Main Concern | Recommended Action

Also explain if any table should replace or complement the 17 tables already explored previously.

Do not modify the Excel file yet. First provide the analysis and recommended shortlist for my review.
