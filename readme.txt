Use this Copilot prompt:

> Read member_retention_ml_copilot_instructions.md and review the latest behavioural_features_business_review.sql.

Open the existing Word document:

Member_Retention_Behavioural_Feature_List.docx

Update the existing behavioural feature table in that document using the latest feature list from behavioural_features_business_review.sql.

Do not create a new Word document.

Do not change the document title, introductory text, source table summary, or existing formatting unless required to fit new rows cleanly.

What to update

Compare the current Word feature table against the latest standalone feature SQL.

Add any newly introduced behavioural features that are not already present in the Word document.

This includes the recently added/reviewed areas such as:

- rollover destination behaviour
- Employer SG baseline/recent/change signals
- Salary Sacrifice baseline/recent/change signals
- Member Voluntary baseline/recent/change signals
- rollover-in related behaviour
- contribution spike/drop/inactivity signals where actually defined
- current FY vs previous FY contribution-change features
- advice engagement features
- low-balance related feature if currently listed in the SQL
- any other new behavioural feature added since the Word document was last created

Do not add features that are only discussed as ideas but are not actually present in the latest behavioural_features_business_review.sql.

Existing table columns

Keep the same columns:

1. S.No
2. Behaviour Name
3. Behaviour Type
4. Description
5. Sample Value
6. Source
7. Comments

Rules for newly added rows

For every feature that is newly added to the Word document:

- populate the normal feature details
- set the Comments column exactly to:

Newly added

For features that already existed in the Word document:

- keep the existing row
- do not mark them as Newly added
- keep their Comments column unchanged

Description style

Keep descriptions very simple and business-friendly.

Use one short sentence in layman English.

Examples:

- Compares recent employer contributions with the member's earlier contribution level.
- Shows whether salary sacrifice contributions have reduced recently.
- Shows whether the member had advice-related engagement during the last 12 months.
- Shows the type of external rollover destination used by the member.

Do not include SQL logic in the description.

Leakage/review features

If a feature is present in the standalone SQL but marked:

- REVIEW REQUIRED
- LEAKAGE REVIEW REQUIRED
- REVIEW REQUIRED - ADDITIONAL SOURCE DEPENDENCY

still include it in the Word document because the document is for business review.

In those cases, keep Comments = Newly added if it is a new row. Do not replace it with technical leakage notes unless the existing table has another dedicated status column.

Source

Use the main business source table only, for example:

- Edge.accountMoneyInflow
- Edge.accountNetMoneyFlow
- Edge.accountRolloverPayment
- Edge.accountEngagementHelpline
- Edge.accountEngagementWorkflow
- Edge.campaignEventDetails / campaignEvents

Follow the existing naming style already used in the Word document.

Sample values

Use simple illustrative values only, such as:

- 1200
- 25% decrease
- Yes / No
- 2 events
- External

Do not invent realistic-looking production values.

Final validation

Before saving, confirm:

- all latest behavioural features in behavioural_features_business_review.sql are represented in the Word feature table
- no duplicate rows exist
- existing rows are preserved
- only newly added rows have Comments = Newly added
- numbering is sequential
- descriptions remain easy for business users to understand
- no churn target, exit field, eligibility flag, or technical validation field has been added as a behaviour

Save the updated document using the same filename:

Member_Retention_Behavioural_Feature_List.docx

Stop after updating and validating the existing Word document.
