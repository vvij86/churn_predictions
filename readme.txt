Please create a new Word document based on the latest standalone feature queries in:

behavioural_features_business_review.sql

The purpose is to prepare a simple business-review document containing all currently identified ML behavioural features.

Important:
- Use the latest SQL in behavioural_features_business_review.sql as the source of truth.
- Do NOT rely on older feature lists if they differ from the latest SQL.
- Extract only the final output features from each standalone query.
- Do not include temporary CTE columns, helper columns, filter columns, raw source columns, or intermediate calculations.
- Do not invent any feature that is not present in the latest SQL.
- If a feature was removed from the latest SQL, do not include it.
- Include all feature groups currently present in the file, including Helpline, Website, Workflow, Campaign/Event, Contribution/Money Inflow, Rollover, Investment, Insurance, Third Party Authority, accountNetMoneyFlow, and any other final feature group actually present in the SQL.
- Keep the wording business-friendly and easily understandable by a non-technical business user.
- Do not use SQL terminology in the Description unless absolutely necessary.

Create one table with these columns:

1. S.No
2. Behaviour Name
3. Behaviour Type
4. Description
5. Sample Value
6. Source
7. Comments

Column guidance:

S.No
- Sequential number starting from 1.

Behaviour Name
- Convert the SQL feature name into a readable business name.
- Example:
  recent_net_flow_90d -> Recent Net Money Flow – 90 Days
  days_since_last_negative_flow -> Days Since Last Negative Money Flow

Behaviour Type
- Use a clear high-level category such as:
  Helpline Engagement
  Website Engagement
  Workflow Activity
  Campaign / Event Behaviour
  Contribution Behaviour
  Rollover / Withdrawal Behaviour
  Investment Behaviour
  Insurance Behaviour
  Third Party Authority
  Net Money Flow Behaviour

Description
- Explain what the feature means in one short sentence.
- Use very simple layman English.
- Explain the business meaning, not how SQL calculates it.
- Examples:
  “Total contribution amount received during the last 12 months.”
  “Number of days since the member last had a negative net money flow.”
  “Shows whether net money flow in the latest 90 days is lower than in the previous 90 days.”

Sample Value
- Provide a realistic illustrative value only.
- Counts: e.g. 5
- Amounts: e.g. $12,500
- Days: e.g. 45 days
- Flags: Yes / No
- Percentages if applicable.
- Sample values are illustrative only and do not need to come from production data.

Source
- Use the actual source table/view from the SQL.
- Example:
  Edge.accountEngagementHelpline
  Edge.accountEngagementWorkflow
  Edge.accountMoneyInflow
  Edge.accountRolloverPayment
  Edge.accountInvestments
  Edge.AccountInsuranceCurrent
  Edge.thirdPartyAuthority
  Edge.accountNetMoneyFlow
  Edge.campaignEventDetails / Edge.campaignEvents
- If a feature uses more than one source, list both.

Comments
- Leave this column completely blank for business review.

Additional requirements:
- Remove obsolete features that are no longer present in the latest standalone SQL.
- For example, if Repeat Helpline Contact Flag has been removed/replaced by inquiry-description-based features, do not keep the old feature.
- Use the latest refined workflow features based on meaningful/member-driven job descriptions.
- Use the latest campaign/event features after excluding rollover-related and leakage-prone events.
- Use the latest contribution and net-money-flow features.
- Use the latest partial-rollover feature set.
- Use the latest investment position-as-of features based on the newest investmentDate available on or before AsOfDate.
- Use the latest insurance features from AccountInsuranceCurrent.
- Use the latest Third Party Authority features.
- Ensure 12-month, 90-day, recency and change/decline features are included where they currently exist in the SQL.
- Do not add a 30-day feature unless it actually exists in the latest SQL.

Document title:
Member Retention ML – Behavioural Feature List

Suggested filename:
Member_Retention_ML_Behavioural_Feature_List.docx

Formatting:
- Landscape orientation if required to fit all columns clearly.
- Use a professional table style with bold header row.
- Repeat the header row across pages.
- Keep font readable.
- Auto-fit column widths appropriately.
- Do not create separate tables per feature group. Keep all behavioural features in one continuous table.

Before creating the Word file, first scan the entire behavioural_features_business_review.sql file and identify the complete final feature list. Then create the document from that latest list.
