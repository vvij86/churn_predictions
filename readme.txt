Please recreate the behavioural feature review Word document using the current final version of:

"behavioural_features_business_review.sql"

The current validated final retained feature count is:

114 features

Important:

- Use the current SQL file as the only source of truth.
- Do not use the old Word document as the source of feature names.
- Do not restore removed features.
- Count and document only the final feature columns returned by the final SELECT of each standalone query.
- Do not include:
  - CTE/helper columns
  - intermediate calculations
  - source-only columns
  - accountID
  - AsOfDate
  - eligibility fields
  - duplicated aliases
  - removed features
  - analysis/debug fields

Create a new Word document. Do not overwrite the previous Word document.

Document title:

"Member Retention ML – Behavioural Feature List"

Suggested filename:

"Member_Retention_ML_Behavioural_Feature_List_Final.docx"

IMPORTANT DOCUMENT STRUCTURE

Do not create one large table containing a repeated "Behaviour Type" column.

Instead:

- Create a separate section for each behaviour type / feature group.
- Under each section, create a separate table containing only the features for that group.
- Use the behaviour type as the section heading.
- Remove the "Behaviour Type" column completely from the tables.

This is intended to make the document easier for business users to read and review.

Create the sections in this order:

1. Helpline Engagement
2. Website Engagement
3. Workflow Activity
4. Campaign / Event Behaviour
5. Contribution Behaviour
6. Rollover / Withdrawal Behaviour
7. Investment Behaviour
8. Insurance Behaviour
9. Third Party Authority
10. Net Money Flow Behaviour

Each section should have its own table.

Table Columns

Each table should contain only these columns:

1. S.No
2. Behaviour Name
3. Description
4. Sample Value
5. Source
6. Comments

Do not include a "Behaviour Type" column.

S.No

Use one continuous serial-number sequence across the entire document from 1 to 114.

Do not restart numbering within each behaviour group.

Example:

- Helpline may contain S.No 1–20
- Website may continue from 21
- Workflow continues after Website
- and so on

Behaviour Name

Convert each SQL feature name into a clear business-readable name.

Examples:

"recent_net_flow_90d"
→ "Recent Net Money Flow – 90 Days"

"days_since_last_negative_flow"
→ "Days Since Last Negative Money Flow"

"recent_complaint_flag_30d"
→ "Recent Complaint Flag – 30 Days"

Description

Write one short, simple, layman-friendly sentence explaining what the feature means.

Explain the business meaning, not the SQL calculation.

Examples:

"contribution_amount_12m"
→ "Total contribution amount received during the last 12 months."

"days_since_last_contribution"
→ "Number of days since the member last made a qualifying contribution."

"recent_complaint_flag_30d"
→ "Shows whether the member raised a complaint during the most recent 30 days."

"net_flow_decline_flag"
→ "Shows whether recent net money flow is lower than in the previous comparison period."

Descriptions must be understandable by non-technical business users.

Avoid technical SQL terms such as:

- CTE
- CASE
- JOIN
- aggregation
- alias

unless absolutely necessary.

Sample Value

Use realistic illustrative values only.

Examples:

- Counts → "5"
- Amount → "$12,500"
- Days → "45 days"
- Flag → "Yes / No"
- Percentage → "-18%"

Sample values are illustrative only and do not need to come from production data.

Source

Use the actual source table/view from the current SQL.

Examples:

- "Edge.accountEngagementHelpline"
- "Edge.accountEngagementWeb"
- "Edge.accountEngagementWorkflow"
- "Edge.campaignEventDetails / Edge.campaignEvents"
- "Edge.accountMoneyInflow"
- "Edge.accountRolloverPayment"
- "Edge.accountInvestments"
- "Edge.AccountInsuranceCurrent"
- "Edge.thirdPartyAuthority"
- "Edge.accountNetMoneyFlow"

Use the exact source naming already present in the SQL.

Comments

Leave this column completely blank for business review.

Do not populate:

- Include
- Exclude
- Pending
- comments
- notes
- recommendations

The business reviewers will use this column later.

Current Final Feature Rules

The final document must reflect the current 114-feature SQL after the reduction exercise.

Retain useful recent behaviour features where they exist:

- 12-month baseline behaviour
- 90-day recent behaviour
- selective 30-day very recent behaviour

Do not remove recent features merely because another time-window version exists.

The restored campaign/event website-login features must be included:

- "website_login_count_12m"
- "website_login_count_90d"
- "website_login_count_30d"
- "days_since_last_website_login"

Also include:

- "insurance_opt_in_12m_flag"

Do not reintroduce any other previously removed features.

Do not include:

- "other_review_event_count_12m"
- invalid investment change-event features
- removed duplicate contribution derivatives
- removed analysis-only features
- churn target/outcome fields
- "MEMBER_EXIT"
- full/external rollover leakage features

Expected Feature Group Counts

Before creating the Word document, validate the extracted list against these exact counts:

- Helpline Engagement = 20
- Website Engagement = 4
- Workflow Activity = 14
- Campaign / Event Behaviour = 21
- Contribution Behaviour = 25
- Rollover / Withdrawal Behaviour = 5
- Investment Behaviour = 3
- Insurance Behaviour = 7
- Third Party Authority = 5
- Net Money Flow Behaviour = 10

Total = 114

If the count does not equal 114:

- do not silently create the document
- report the discrepancy
- identify which group count differs

Section Format

For each behaviour group:

1. Add a clear heading.
2. Optionally add a very short one-line description of what that behaviour group represents.
3. Add the feature table immediately below it.

Example:

"1. Helpline Engagement"

"Features describing how frequently and recently the member contacted the helpline and the types of enquiries raised."

Then add the table.

Use similar simple introductory sentences for the other groups.

Word Formatting

Create a new ".docx" file.

Formatting requirements:

- Use clear section headings for each behaviour type.
- Use landscape orientation if it improves table readability.
- Use a professional table style.
- Bold the header row.
- Repeat the table header row when a table continues across multiple pages.
- Keep fonts readable.
- Auto-fit column widths sensibly.
- Give more width to "Behaviour Name", "Description", and "Source".
- Keep "S.No" and "Sample Value" relatively narrow.
- Keep a reasonable-width "Comments" column for business reviewers.
- Avoid splitting a single table row across pages where possible.
- Add spacing between behaviour sections.
- Keep formatting consistent across all 10 tables.

Do not create one giant table.

Create 10 separate business-friendly tables, one for each behaviour group.

Final Validation

After creating the document, verify:

- total feature count = 114
- all 10 feature groups are present
- each group's count matches the expected count
- numbering runs continuously from 1 to 114
- no Behaviour Type column exists
- Comments column is blank
- only current final SQL features were included
- restored website-login and insurance-opt-in features are present
- removed features are not present

Then report:

- created filename
- total feature count
- number of behaviour-group tables
- count per group
- confirmation that Comments is blank
- confirmation that numbering is continuous from 1 to 114
- confirmation that "Behaviour Type" was removed from the table structure.
