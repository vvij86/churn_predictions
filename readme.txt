Read and use the following project files as the source of truth:

- member_retention_ml_copilot_instructions.md
- behavioural_features_business_review.sql
- MemberRetention_01-AccountBase_v006.sql
- MemberRetention_03-MemberRetentionMetrics_v005.sql
- All_table_scripts.sql
- All_Other_tables_Not_explored.sql

Create a new Word document that explains the historical training snapshot, AsOfDate, feature window, outcome window, training/validation split, and untouched test-period approach for the Member Retention ML model.

The document must be easy to understand for both technical and non-technical/business users.

Suggested filename:

Member_Retention_ML_Historical_Training_and_Snapshot_Approach.docx

Suggested title:

Member Retention ML – Historical Training, Snapshot and Validation Approach


---

1. Purpose

Start with a short business-friendly explanation of why historical snapshots are required.

Explain that the model must learn from what was known about an account at a particular point in time and then observe whether the account churned in the following outcome period.

Explain in simple terms:

Past behaviour → AsOfDate/Snapshot → Future churn outcome

Avoid overly technical ML terminology.


---

2. Historical Data Period

Explain that historical data starts from:

1 April 2023

The standard feature window is:

12 months

The churn outcome window is:

3 months

Explain that because a complete 12-month feature history is required, the first full snapshot can be:

31 March 2024


---

3. Snapshot / AsOfDate Logic

Clearly explain:

Snapshot Date = AsOfDate

Explain in simple English that AsOfDate acts as a cut-off date.

For each snapshot, the model must only use information that was known on or before that AsOfDate.

Anything occurring after AsOfDate must not be used as a predictive feature.

Include a simple example:

Feature history → AsOfDate → Future outcome

Example:

01-Apr-2023 to 31-Mar-2024 → AsOfDate 31-Mar-2024 → Outcome 01-Apr-2024 to 30-Jun-2024


---

4. Account Eligibility Using fundJoinDate

Explain how fundJoinDate is used to determine whether an account existed at a particular snapshot.

Use:

fundJoinDate <= AsOfDate

Give a simple example:

For AsOfDate = 30-Jun-2024:

- Account joined 10-Jan-2022 → Included
- Account joined 15-Jun-2024 → Included
- Account joined 10-Jul-2024 → Not included

Explain that an account cannot be included in a historical snapshot before it actually joined the fund.

Also explain that exit eligibility uses the approved exit logic from the project instructions and that future exit information must not be used as a feature.


---

5. Exact Date Columns Used by Feature Group

This section is very important.

Do not invent generic date columns.

Read the latest behavioural_features_business_review.sql, DDL files and business reference SQL and identify the exact physical date column actually used for each feature group.

Create a table with:

| S.No | Feature Group | Source Table | Date Column Used | How It Is Compared With AsOfDate | Example |

Include feature groups such as:

- Helpline
- Workflow
- Web
- Contributions / Money Inflow
- Net Money Flow
- Rollover / Withdrawal
- Investment behaviour
- Insurance where applicable
- Third Party Authority
- Campaign / Event behaviour
- any other feature group currently present in behavioural_features_business_review.sql

For each feature group, trace the actual date column from the SQL.

Examples of the type of explanation expected:

callDate between FeatureStartDate and AsOfDate

processedDate between FeatureStartDate and AsOfDate

referenceDate between FeatureStartDate and AsOfDate

These are examples only. Use the actual column names from the current SQL.

If a table does not have a reliable historical/effective date for a feature, explicitly state:

Point-in-time limitation / business confirmation required

Do not guess.


---

6. Feature Window

Explain that most behavioural features use the previous 12 months relative to each AsOfDate.

Use:

FeatureStartDate = day after AsOfDate minus 12 months

Give an easy example:

AsOfDate:

30-Jun-2024

Feature Window:

01-Jul-2023 to 30-Jun-2024

Explain that helpline contacts, contributions, workflows, rollover activity and other behaviours are calculated only from this period unless a feature has a specifically approved shorter comparison period such as 90 days.


---

7. Outcome / Target Window

Explain the 3-month outcome window.

For example:

AsOfDate:

30-Jun-2024

Outcome:

01-Jul-2024 to 30-Sep-2024

Explain:

- qualifying churn in outcome window → target_churn = 1
- no qualifying churn → target_churn = 0

Use the approved exitDateRecorded logic from the project instructions.

Make it very clear that the outcome-period information is used only to create the training label and is not used as an input feature.


---

8. Historical Snapshot Table

Create a visually clear table similar to the sample screenshot/reference I have provided.

Use columns:

| Snapshot | Feature Start Date | AsOfDate | Outcome Start Date | Outcome End Date |

Start from:

01-Apr-2023

Use quarterly snapshots initially for the illustration because they are easier for business users to understand.

Include a table similar to:

| Snapshot | Feature Start Date | AsOfDate | Outcome Start Date | Outcome End Date | | 1 | 01-Apr-2023 | 31-Mar-2024 | 01-Apr-2024 | 30-Jun-2024 | | 2 | 01-Jul-2023 | 30-Jun-2024 | 01-Jul-2024 | 30-Sep-2024 | | 3 | 01-Oct-2023 | 30-Sep-2024 | 01-Oct-2024 | 31-Dec-2024 | | 4 | 01-Jan-2024 | 31-Dec-2024 | 01-Jan-2025 | 31-Mar-2025 | | 5 | 01-Apr-2024 | 31-Mar-2025 | 01-Apr-2025 | 30-Jun-2025 | | 6 | 01-Jul-2024 | 30-Jun-2025 | 01-Jul-2025 | 30-Sep-2025 | | 7 | 01-Oct-2024 | 30-Sep-2025 | 01-Oct-2025 | 31-Dec-2025 | | 8 | 01-Jan-2025 | 31-Dec-2025 | 01-Jan-2026 | 31-Mar-2026 |

Extend further only where the required outcome data is available.

Validate all dates carefully.

Below the table add notes:

- Each snapshot uses the previous 12 months to calculate features.
- target_churn is determined only from the following 3-month outcome window.
- Snapshot outputs are combined to create the historical modelling dataset.
- The same account may appear in multiple snapshots with different AsOfDate values.
- The production pipeline may run monthly even though quarterly snapshots are shown here for easy illustration.


---

9. Monthly Production Snapshot

Explain that although the historical illustration uses quarterly snapshots for simplicity, the production pipeline is expected to run monthly.

Give an example:

31-Mar-2026

30-Apr-2026

31-May-2026

etc.

Explain that each monthly pipeline run recalculates features based on that month's AsOfDate.


---

10. 80/20 Training and Validation Approach

Explain in simple terms that the data should not be randomly split at row level.

Use a time-based 80/20 split.

Explain:

- approximately the earliest 80% of eligible historical snapshots are used for model development
- approximately the latest 20% is reserved for independent testing

Explain why:

The same account may appear in several historical snapshots, so random splitting could place different versions of the same account in both training and testing and give an overly optimistic result.

Use a simple timeline illustration:

Earlier historical snapshots → Train / Validate

Latest historical snapshots → Untouched Test


---

11. Untouched Test Period

Explain clearly what "untouched" means.

The untouched test period must not be used for:

- feature selection
- algorithm selection
- hyperparameter tuning
- probability threshold selection
- model comparison

It should only be used once the final model approach is selected.

If data is available through a particular latest date, determine the latest AsOfDate that still has the complete 3-month outcome window.

Do not assume that the most recent available source date can automatically be used as a test snapshot.

For example, an AsOfDate requires three additional months of future outcome data before its target can be fully known.


---

12. Training / Validation / Final Test Flow

Add a simple flow such as:

Historical source data

↓

Create point-in-time snapshots

↓

Calculate behavioural features using dates <= AsOfDate

↓

Create target using next 3 months

↓

Combine historical snapshots

↓

Earlier ~80% → Training / Validation

↓

Latest ~20% → Untouched Final Test

↓

Final model evaluation

Make this visually easy to understand.


---

13. Simple End-to-End Example

Include one example account.

Example:

Account joined:

15-Jan-2022

Snapshot / AsOfDate:

30-Jun-2024

Feature window:

01-Jul-2023 to 30-Jun-2024

Helpline contacts:

only contacts during the feature window

Contributions:

only contributions during the feature window

Rollover:

only eligible rollover events on or before AsOfDate

Outcome window:

01-Jul-2024 to 30-Sep-2024

If qualifying exitDateRecorded occurs on 20-Aug-2024:

target_churn = 1

Explain that the 20-Aug-2024 exit is used only as the target outcome and must never appear as a feature for the 30-Jun-2024 snapshot.


---

Formatting Requirements

Make the Word document professional and easy for business users to read.

Use:

- clear section headings
- concise paragraphs
- tables where useful
- bold key dates and rules
- simple flow diagrams using Word shapes if practical
- the historical snapshot table as a prominent visual

Avoid excessive technical language.

Where technical terms such as AsOfDate, Feature Window, Outcome Window, or Untouched Test Set are used, explain them immediately in simple English.

Do not change any existing project files.

Do not modify behavioural_features_business_review.sql.

This task is only to create the explanatory Word document.

Before finishing, validate:

- all physical date-column names against the actual SQL/DDL
- all snapshot dates
- 12-month feature-window calculations
- 3-month outcome-window calculations
- AsOfDate point-in-time logic
- fundJoinDate eligibility logic
- exitDateRecorded target logic
- no future information is described as a predictive feature
- training/test split is chronological, not random

Save as:

Member_Retention_ML_Historical_Training_and_Snapshot_Approach.docx
