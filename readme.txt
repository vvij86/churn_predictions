Create a new Functional Requirements Specification (FRS) document for the Tactical ML Churn / Member Retention approach.

FINAL DELIVERABLE:
Create the final output as a Microsoft Word document (.docx).

Suggested filename:
Tactical_ML_Churn_FRS.docx

IMPORTANT:
- This FRS must cover ONLY the ML-related Tactical approach.
- Do not mix in non-ML project requirements.
- Use the business clarification tracker:
  Clarifications_Internal(1).xlsx
  as the primary source of truth for confirmed decisions, open questions, resolutions and comments.
- Also use the attached sample account-level churn prediction output as a reference for the ML output section.
- Preserve the business wording and intent from the clarification tracker.
- Do not invent business decisions where the tracker is still open.
- Do not silently convert an Open item into Confirmed.
- For unresolved items, clearly mark:
  "Open / Pending Business Confirmation"
- Keep unresolved comments visible in the FRS.
- Every major FRS requirement must contain a simple example.
- Keep the language business-friendly and understandable for Business, BA, Data Modeller, Data Scientist and Power BI reviewers.
- Do not include detailed SQL, Python, PySpark or model implementation code.
- The FRS should represent the Tactical approach using MercerEdge source data / approved Bronze-layer source mappings for ML churn prediction.

Suggested document title:

"Functional Requirements Specification – Member Retention / Churn Prediction – Tactical ML Approach"


==================================================
WORD DOCUMENT FORMAT
==================================================

Create the final deliverable as a professional Microsoft Word document (.docx).

Suggested filename:
Tactical_ML_Churn_FRS.docx

Use:
- Professional title page
- Document title
- Version
- Date
- Prepared By, if available
- Table of Contents
- Numbered headings and subheadings
- Professional tables
- Consistent fonts and spacing
- Page numbers
- Header/footer where appropriate
- Clear section numbering
- Business-friendly formatting

Do not return only Markdown or plain text.
Save the completed FRS as a .docx file.


==================================================
1. DOCUMENT PURPOSE
==================================================

Explain that this FRS defines the functional requirements for the Tactical ML churn / member retention solution.

Cover:
- Account-level churn prediction
- Modelling population
- Churn and retention definitions
- Feature engineering
- Date/window logic
- Eligibility rules
- Behavioural/customer features
- Point-in-time safety
- Leakage controls
- Validation approach
- Risk scoring
- Churn drivers
- ML scoring output
- Power BI consumption


==================================================
2. SCOPE
==================================================

In Scope:
- Account-level churn prediction
- Historical modelling dataset preparation
- Feature engineering
- Churn target definition
- Retention definition
- Modelling eligibility
- Feature Window
- AsOfDate / prediction snapshot
- Outcome Window
- Behavioural features
- Customer experience features
- Point-in-time safety
- Target leakage controls
- Model validation approach
- Risk bands
- Primary/additional churn drivers
- ML scoring output
- Power BI consumption

Out of Scope:
- Strategic source redesign
- Non-ML dashboard requirements
- Detailed production infrastructure implementation
- Detailed Databricks implementation
- Detailed SQL / PySpark / model code


==================================================
3. TERMS / DEFINITIONS / GLOSSARY
==================================================

Create a dedicated table near the beginning of the document.

Use columns:

Term / Acronym
Definition
Simple Example / Business Meaning

Include at least:

- ML
- Churn
- Retention
- target_churn
- Account
- Member
- Modelling Grain
- Feature
- Feature Engineering
- Behavioural Feature
- AsOfDate
- Prediction Date
- FeatureStartDate
- FeatureEndDate
- Feature Window
- Lookback Period
- OutcomeStartDate
- OutcomeEndDate
- Outcome Window
- Prediction Horizon
- Churn Probability
- Risk Score
- Risk Band
- High Risk
- Medium Risk
- Low Risk
- Primary Churn Driver
- Additional Churn Drivers
- Retention Category
- Internal Transfer
- Partial Rollover
- Full Rollover
- Partial Withdrawal
- Point-in-Time
- Point-in-Time Safety
- Target Leakage
- Data Leakage
- Eligibility
- Modelling Population
- Historical Snapshot
- Time-Based Validation
- Validation Set
- Test / Holdout Set
- Fold
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix
- FUM
- CSAT
- NPS
- VoC
- Bronze Layer
- Tactical Approach
- Strategic Approach
- ML Scoring
- Model Version
- Persisted ML Output
- Power BI Consumption

Keep definitions short and business-friendly.

Example:

Term:
AsOfDate

Definition:
The date at which account/member information is frozen for prediction. Only information available on or before this date can be used as predictive input.

Example:
31-Mar-2024


==================================================
4. REQUIREMENT FORMAT
==================================================

For every major functional requirement, use a consistent structure/table with:

- Requirement ID
- Requirement Name
- Requirement Description
- Business Rule / Current Position
- Example
- Status
- Comments / Open Points

Use IDs such as:

FR-ML-001
FR-ML-002
FR-ML-003
...

Allowed statuses:

- Confirmed
- Proposed
- Open
- Deferred
- Review Required


==================================================
5. MODELLING GRAIN
==================================================

Requirement:
One row per account_id per AsOfDate.

Use the clarification tracker to confirm status.

Example:
account_id = A001
AsOfDate = 31-Mar-2024

One modelling record should exist for this account and snapshot date.


==================================================
6. CHURN DEFINITION
==================================================

Use the confirmed business resolution from Clarifications_Internal(1).xlsx.

Current understood rule:
Churn is identified using account exitDate, provided the exit is not an internal transfer.

Use the approved internal transfer logic / internalTransferFlag exclusion.

Example:
AsOfDate = 31-Mar-2024
Outcome Window = 01-Apr-2024 to 30-Jun-2024

exitDate = 15-May-2024
internalTransferFlag = 0

Result:
target_churn = 1

Example 2:
exitDate = 15-May-2024
internalTransferFlag = 1

Result:
Not treated as normal churn / excluded according to the approved business rule.


==================================================
7. RETENTION DEFINITION
==================================================

Define retention based on the business clarification tracker.

Current understood rule:
An eligible account is retained when no qualifying churn event occurs during the outcome window.

Example:
AsOfDate = 31-Mar-2024
Outcome Window = 01-Apr-2024 to 30-Jun-2024
No qualifying exit occurs

Result:
target_churn = 0


==================================================
8. PARTIAL ROLLOVER / PARTIAL WITHDRAWAL
==================================================

Use the business tracker resolution.

Current understood position:
Partial rollover / partial withdrawal may be used as a churn-risk feature and should not itself be treated as the final churn target.

Example:
A member makes a partial rollover before AsOfDate.

This activity may be used as a predictive behavioural feature.


==================================================
9. DEATH-RELATED EXITS
==================================================

Use the confirmed business rule.

Current understood rule:
Death-related exits must be excluded from normal churn modelling.

Example:
If a valid dateOfDeath exists and the exit is death-related, the account must not be labelled as ordinary churn.


==================================================
10. ACCOUNT ELIGIBILITY
==================================================

Use the clarification tracker.

Include:
- AccountSummary requirement
- fundJoinDate
- historical account existence
- newly joined accounts
- minimum tenure, if any

Current understood position:
Newly joined accounts should be included unless business confirms a minimum tenure requirement.

Example:
fundJoinDate = 01-Mar-2024
AsOfDate = 31-Mar-2024

The account may still be included with approximately one month of history.


==================================================
11. ACCOUNTSUMMARY REQUIREMENT
==================================================

Document the confirmed rule from the clarification tracker on whether AccountSummary is mandatory for modelling eligibility.

Do not invent a decision if this is still open.

Include an example showing how an account is handled when AccountSummary information is unavailable.


==================================================
12. FEATURE WINDOW / FEATURE DATE RANGE
==================================================

Create a dedicated requirement.

Definition:
The historical period before AsOfDate used to calculate predictive features.

Business question:
How much past member/account behaviour should be used?

Current proposed approach:
Previous 12 months before AsOfDate.

Example:
AsOfDate = 31-Mar-2024
FeatureStartDate = 01-Apr-2023
FeatureEndDate = 31-Mar-2024

Include:
- FeatureStartDate
- FeatureEndDate
- Lookback duration
- Treatment of newly joined accounts with shorter history

If not confirmed in the tracker:
Status = Open / Pending Business Confirmation


==================================================
13. ASOFDATE / PREDICTION DATE
==================================================

Create a dedicated requirement.

Definition:
AsOfDate is the historical prediction cut-off date.

Only information available on or before AsOfDate can be used as predictive input.

Clearly state:

AsOfDate is NOT derived from fundJoinDate.

fundJoinDate is used only to:
- confirm the account existed by AsOfDate
- derive tenure

Business question:
Should prediction snapshots be:
- Monthly
- Quarterly
- Year-end
- Another frequency

Examples:
31-Mar-2024
30-Jun-2024
30-Sep-2024
31-Dec-2024

If snapshot frequency is still open, keep it as Open.


==================================================
14. OUTCOME WINDOW
==================================================

Create a dedicated requirement.

Definition:
The future period after AsOfDate during which churn is observed for creation of target_churn.

Proposed approach:

OutcomeStartDate = AsOfDate + 1 day
OutcomeEndDate = AsOfDate + 3 months

Example:
AsOfDate = 31-Mar-2024
OutcomeStartDate = 01-Apr-2024
OutcomeEndDate = 30-Jun-2024

If a qualifying churn occurs during the period:
target_churn = 1

If no qualifying churn occurs:
target_churn = 0

If the 3-month duration is not yet confirmed:
Status = Open / Pending Business Confirmation


==================================================
15. OUTCOME START DATE
==================================================

Document the business decision regarding outcome start.

Current understood position:
Outcome observation begins the day after AsOfDate.

Example:
AsOfDate = 31-Mar-2024
OutcomeStartDate = 01-Apr-2024


==================================================
16. DATE RELATIONSHIP / TIMELINE
==================================================

Include a simple visual timeline or professional table showing:

Feature Window:
01-Apr-2023 to 31-Mar-2024

AsOfDate:
31-Mar-2024

Outcome Window:
01-Apr-2024 to 30-Jun-2024

Show:

[ Historical Feature Window ]
            ->
[ AsOfDate / Prediction Date ]
            ->
[ Outcome / Churn Observation Window ]

Also explain:

Feature Window = historical behaviour used as model input

AsOfDate = prediction cut-off date

Outcome Window = future observation period used only for target creation


==================================================
17. BEHAVIOURAL / CUSTOMER FEATURES
==================================================

Create a dedicated section.

Use the clarification tracker and current tactical feature-engineering design.

Keep it business-friendly.


A. HELPLINE ENGAGEMENT

Possible features:
- Days since last helpline contact
- Helpline contact count
- Helpline inquiry count

Example:
Previous 12-month helpline contacts = 5
Days since last helpline contact = 20


B. WEBSITE ENGAGEMENT

Possible features:
- Website visit/activity count
- Days since last website activity

Important UAT limitation:

accountEngagementWeb is not populated in UAT.

Therefore:
- Do not interpret UAT NULL values as zero web activity.
- Keep web features in scope.
- State that they require revalidation using Prod / Databricks source where data is available.

Example:
Website activities in previous 12 months = 8
Days since last web activity = 15


C. WORKFLOW ACTIVITY

Possible features:
- Workflow completion count
- Open workflow count
- Days since last workflow job

Note:
Workflow data may contain noisy/non-useful workflow types.

If business still needs to confirm useful workflow types:
Status = Open / Pending Business Confirmation

Example:
Completed workflows = 3
Open workflows = 1


D. CAMPAIGN ENGAGEMENT

Use the latest business clarification.

If the tracker states:
"Park it for case 2 / Not needed as of now"

Then set:

Status = Deferred / Future Consideration

Do NOT present it as an active confirmed tactical feature.

Possible future features:
- Email sent/opened/clicked
- Engagement rate
- Days since campaign interaction

Example:
Campaign open count = 6


E. CONTRIBUTION / MONEY FLOW BEHAVIOUR

Possible features:
- Contribution count
- Total contribution amount
- Average contribution amount
- Net money flow
- Negative net flow count
- Declining contribution/inflow indicators

Example:
Contribution count in previous 12 months = 10
Recent contribution amount is lower than the previous comparison period.


F. ROLLOVER / WITHDRAWAL BEHAVIOUR

Possible features:
- Partial rollover count
- Partial rollover amount
- External rollover activity, where appropriate

Example:
Two partial rollover events before AsOfDate may indicate elevated churn risk.


G. CUSTOMER EXPERIENCE / VOC – QUALTRICS

Keep this at a high level.

Include:
- CSAT score
- NPS score
- Survey / feedback recency

Business question:
Can Qualtrics CSAT / NPS / VoC measures be used as customer-experience features for churn prediction?

If not confirmed:
Status = Open / Pending Business and Source Confirmation

Example:
Latest CSAT score available before AsOfDate may be used as a customer-experience signal.


==================================================
18. FEATURE LEAKAGE / POINT-IN-TIME RULE
==================================================

Create a mandatory ML requirement.

Rule:
Only information available on or before AsOfDate can be used as predictive input.

Do NOT use future outcome information as features.

Examples of prohibited predictive inputs:
- future exitDate
- MEMBER_EXIT
- future account closure
- future full rollover completion
- future churn outcome
- any event after AsOfDate

Example:
AsOfDate = 31-Mar-2024
EventDate = 15-Apr-2024

The event must NOT be used as a feature for the 31-Mar-2024 prediction.


==================================================
19. MODEL VALIDATION APPROACH
==================================================

Create a dedicated FRS section.

Recommended approach:
Time-based validation rather than random splitting.

Business-friendly explanation:
The model should learn from older historical data and be tested on later periods so that the validation better represents real future prediction.

If not formally confirmed:
Status = Proposed / Open


==================================================
20. TIME-BASED VALIDATION EXAMPLE
==================================================

Use the proposed example where appropriate:

Fold 1:
Train up to 31-Dec-2024
Validate Jan-Mar 2025

Fold 2:
Train up to 31-Mar-2025
Validate Apr-Jun 2025

Fold 3:
Train up to 30-Jun-2025
Validate Jul-Sep 2025

Clearly label this as:

Illustrative / Proposed

unless the exact dates are confirmed in the tracker.


==================================================
21. VALIDATION TYPES
==================================================

Create separate subsections.


A. DATA VALIDATION

Include:
- Row count validation
- One row per account_id + AsOfDate
- Duplicate checks
- NULL / missing value checks
- Eligibility checks
- Invalid/impossible value checks

Example:
duplicate account_id + AsOfDate count must be 0.


B. POINT-IN-TIME VALIDATION

Include:
- No features from after AsOfDate
- Future event contribution count must equal 0

Example:
An event dated after AsOfDate cannot be used as a predictive feature.


C. TARGET LEAKAGE VALIDATION

Validate that fields/events such as:
- exitDate
- MEMBER_EXIT
- future rollover completion
- account closure
- outcome-period information

are not predictive model inputs.

Example:
exitDate may be used for creation of target_churn but must not be used as an input feature.


D. FEATURE VALIDATION

Include:
- NULL percentage
- Distinct values
- Constant features
- Near-constant features
- Sparse features
- Historical availability
- Feature availability by environment
- Current-state vs historical validity


E. MODEL VALIDATION

Include:
- ROC-AUC
- Precision
- Recall
- F1 Score
- Confusion Matrix

Do not invent minimum thresholds unless agreed.


F. TIME-BASED VALIDATION

Explain use of older periods for training and later periods for validation/test.


==================================================
22. VALIDATION ACCEPTANCE CRITERIA
==================================================

Include:

- one row per account_id + AsOfDate
- duplicate count = 0
- target definition remains consistent
- future-data leakage = 0
- point-in-time validation passes
- eligibility rules applied correctly
- feature window applied correctly
- outcome window applied correctly
- open business items documented
- model validation meets agreed technical/business criteria


==================================================
23. RISK BANDS
==================================================

Use the proposed starting thresholds:

High:
>= 0.70

Medium:
0.40 to 0.69

Low:
< 0.40

Clearly state:
These are proposed initial thresholds and may change after validation and business review.

Examples:

0.82 -> High
0.55 -> Medium
0.25 -> Low


==================================================
24. ML SCORING / POWER BI CONSUMPTION
==================================================

Use the clarification tracker resolution.

Document whether Power BI should consume persisted ML scoring output.

Preferred requirement wording:

The ML process generates and stores account-level scoring results.
Power BI consumes the latest persisted ML scoring output rather than triggering the model itself.

Example:
Scheduled ML scoring creates the latest account churn predictions.
Power BI reads the resulting output table.


==================================================
25. ML OUTPUT REQUIREMENTS
==================================================

Use the attached sample account-level churn prediction output as a reference.

Include required fields such as:

- reporting_period, if required
- scoring_date, if required
- account_id
- member_id
- as_of_date
- churn_probability
- risk_band
- primary_churn_driver
- additional_churn_drivers
- retention_category
- current_account_fum_amount
- model_version

Add an illustrative sample table.

Example:

account_id | member_id | as_of_date | churn_probability | risk_band | primary_churn_driver | additional_churn_drivers | retention_category | current_account_fum_amount | model_version

A001 | M001 | 31-Mar-2026 | 0.87 | High | Reduced contribution activity | Partial rollover-out activity | At Risk | 150000 | RF_v1

A002 | M002 | 31-Mar-2026 | 0.76 | High | Increased withdrawal activity | Reduced contributions | At Risk | 98000 | RF_v1

A003 | M003 | 31-Mar-2026 | 0.69 | Medium | Partial rollover-out activity | Lower contribution frequency | Monitor | 210000 | RF_v1

Clearly label:
"Illustrative sample output only."


==================================================
26. PRIMARY AND ADDITIONAL CHURN DRIVERS
==================================================

Requirement:
The ML output should provide the primary driver of churn risk and, where available, supporting additional drivers.

Example:

Primary Driver:
Reduced contribution activity

Additional Driver:
Partial rollover activity


==================================================
27. RETENTION CATEGORY
==================================================

Define the proposed business-friendly retention category.

Possible example:

High Risk -> At Risk
Medium Risk -> Monitor
Low Risk -> Retained

If the mapping has not been formally approved:
Status = Open / Pending Business Confirmation


==================================================
28. MODEL VERSION
==================================================

Every scoring output should identify the model version.

Example:
RF_v1

This supports traceability of which model produced each prediction.


==================================================
29. SOURCE SCOPE / TACTICAL APPROACH
==================================================

State that the Tactical ML solution is proceeding with the required sources available through the approved Bronze-layer / source-target mappings.

However:

Final source scope should be closed out with the business before being considered fully finalized.

Do not state that no additional sources are required unless confirmed by business.

Mention Qualtrics separately if its inclusion is still being assessed.


==================================================
30. OPEN COMMENTS / PENDING BUSINESS CONFIRMATION
==================================================

Create a dedicated table.

Columns:

Requirement / Topic
Current Position
Business Resolution
Status
Comments / Open Question

Populate it directly from unresolved/open items in:
Clarifications_Internal(1).xlsx

Include where applicable:

- Feature Window
- AsOfDate frequency
- Outcome Window duration
- Validation approach
- Workflow feature selection
- Campaign behavioural features
- Qualtrics CSAT / NPS usage
- Source/table scope confirmation
- Risk-band thresholds
- Retention category mapping
- Current-state/historical source limitations
- Any feature requiring business interpretation

Do NOT force-close open items.


==================================================
31. ASSUMPTIONS / CONSTRAINTS
==================================================

Include applicable Tactical limitations such as:

- Tactical solution is based on currently approved MercerEdge / Bronze-aligned sources.
- Final source scope requires business close-out.
- Some UAT sources may not contain representative Prod data.
- accountEngagementWeb is not populated in UAT.
- Web engagement features remain in scope but require Prod/Databricks validation.
- Some current-state fields may require historical validation.
- Qualtrics source/usage may require confirmation.
- Campaign engagement is deferred if that is the latest business position.
- Final feature set may change after business validation and model validation.


==================================================
32. FRS ACCEPTANCE CRITERIA
==================================================

The Tactical ML FRS is considered ready when:

- churn definition is confirmed
- retention definition is confirmed
- eligibility rules are confirmed
- Feature Window is confirmed
- AsOfDate / prediction frequency is confirmed
- Outcome Window is confirmed
- behavioural feature scope is confirmed
- Qualtrics/VoC position is documented
- point-in-time leakage rules are accepted
- validation approach is agreed
- scoring output fields are agreed
- risk-band approach is agreed
- source scope is confirmed or explicitly marked open
- all remaining open business clarifications are documented


==================================================
FINAL QUALITY CHECK
==================================================

Before saving the Word document:

1. Compare every Confirmed/Open/Deferred requirement back to Clarifications_Internal(1).xlsx.
2. Do not invent or infer a business decision that is not supported by the tracker.
3. Preserve important business comments from the tracker.
4. Clearly distinguish:
   - Confirmed
   - Proposed
   - Open
   - Deferred
   - Review Required
5. Every major requirement must contain a simple example.
6. Ensure Feature Window, AsOfDate, Outcome Window and their relationship are very clear.
7. Include the timeline:
   Feature Window -> AsOfDate -> Outcome Window
8. Include the full validation approach.
9. Include the Terms / Definitions / Glossary table.
10. Include the attached account-level churn prediction output as an illustrative output example.
11. Keep the FRS ML-focused and Tactical only.
12. Do not include detailed implementation code.
13. Keep unresolved business comments visible.
14. Ensure tables are readable and professionally formatted.
15. Generate the final output as:

Tactical_ML_Churn_FRS.docx

Do not return only plain text or Markdown.
Create and save the completed Microsoft Word document.
