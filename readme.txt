Create a NEW Word document based on the existing Tactical ML Churn FRS.

IMPORTANT:
- Do NOT modify or overwrite the existing FRS document.
- Create a separate new Microsoft Word file.
- Suggested filename:

Tactical_ML_Churn_FRS_Table_Format.docx

Purpose:
Convert the existing Tactical ML Churn FRS into a concise, easy-to-review TABLE-BASED format similar to the attached sample.

The target format should be easy for Business, BA, Data Modeller, Data Engineer, Data Scientist and Power BI teams to review quickly.


TABLE FORMAT
============

Create the main FRS requirements in one consolidated table using columns similar to:

1. Functional Requirement ID
2. Requirement / Description
3. Business Rule / Current Position
4. Example
5. Source / Reference
6. Source Mapping
7. Status
8. Comments / Open Points

Use IDs such as:

FR-ML-001
FR-ML-002
FR-ML-003
...


IMPORTANT:
Do not remove any requirement from the existing FRS.
Convert the existing narrative sections into concise table rows.

Each major requirement should normally be one row or a small number of rows where needed.


CONTENT TO INCLUDE
==================

Include all ML requirements already present in the existing Tactical ML FRS, including:

- Modelling grain
- Churn definition
- Retention definition
- Internal transfer exclusion
- Death-related exit exclusion
- Partial rollover / partial withdrawal treatment
- Account eligibility
- AccountSummary requirement
- Newly joined accounts
- Feature Window
- FeatureStartDate / FeatureEndDate
- AsOfDate
- Outcome Start Date
- Outcome Window
- Feature Window -> AsOfDate -> Outcome Window relationship
- Behavioural features
- Helpline engagement
- Website engagement
- Workflow activity
- Contribution / money flow behaviour
- Rollover behaviour
- Campaign engagement status
- Qualtrics CSAT / NPS / VoC
- Point-in-time safety
- Target leakage
- Data validation
- Feature validation
- Time-based validation
- Model validation
- Risk bands
- Primary churn driver
- Additional churn drivers
- Retention category
- Model version
- ML scoring
- Power BI consumption
- ML output fields
- Tactical source scope
- Bronze / Silver dependency where documented
- Assumptions / constraints
- Open business clarifications
- Acceptance criteria


EXAMPLE COLUMN
==============

Every requirement must contain a short and simple example.

Examples:

Feature Window:
AsOfDate = 31-Mar-2024
Feature Window = 01-Apr-2023 to 31-Mar-2024

Outcome Window:
AsOfDate = 31-Mar-2024
Outcome Window = 01-Apr-2024 to 30-Jun-2024

Churn:
exitDate = 15-May-2024
internalTransferFlag = 0
=> target_churn = 1

Risk Band:
churn_probability = 0.82
=> High Risk


SOURCE / REFERENCE COLUMN
=========================

Populate the Source / Reference column from the existing FRS and available source material.

Examples may include:

- Clarifications_Internal(1).xlsx
- Business clarification tracker
- BRS section reference
- Sample churn prediction output
- MercerEdge source
- Bronze source-target mapping
- Qualtrics, if applicable

Do not invent references.


SOURCE MAPPING COLUMN
=====================

Where a technical source is known, capture it briefly.

Examples:

accountSummary.exitDate
accountRolloverPayment.internalTransferFlag
accountSummary.fundJoinDate
accountEngagementHelpline
accountEngagementWeb
accountMoneyInflow
accountNetMoneyFlow
accountRolloverPayment
Qualtrics – pending confirmation

If the mapping is not yet confirmed, write:

TBD / Pending Source Mapping

Do not guess.


STATUS COLUMN
=============

Use only:

- Confirmed
- Open
- Proposed
- Deferred
- Review Required

Use the existing FRS / clarification tracker as the source of truth.


COMMENTS / OPEN POINTS
======================

Keep unresolved items visible.

Examples:

- Feature Window pending business confirmation
- AsOfDate frequency pending confirmation
- Outcome Window duration pending confirmation
- Workflow useful/noisy event selection pending
- Campaign engagement deferred
- Qualtrics CSAT/NPS pending business/source confirmation
- Web engagement UAT source not populated
- Final source scope pending business close-out


SEPARATE TABLES
===============

In addition to the main Functional Requirements table, create these smaller tables:

1. Terms / Definitions Table

Columns:
- Term
- Definition
- Example / Business Meaning

Include key terms such as:
- Churn
- Retention
- AsOfDate
- Feature Window
- Outcome Window
- target_churn
- Point-in-Time Safety
- Target Leakage
- Time-Based Validation
- Risk Band
- CSAT
- NPS
- VoC
- FUM
- Bronze
- Silver
- Gold
- Model Version


2. Behavioural Feature Summary Table

Columns:
- Feature Group
- Example Features
- Current Status
- Source
- Comments

Include:
- Helpline
- Website
- Workflow
- Contribution / Money Flow
- Rollover
- Campaign
- Customer Experience / Qualtrics


3. Date / Window Summary Table

Columns:
- Item
- Definition
- Proposed / Confirmed Value
- Example
- Status

Include:
- Feature Window
- AsOfDate
- Outcome Start
- Outcome Window
- Snapshot Frequency


4. Validation Summary Table

Columns:
- Validation Type
- What is Checked
- Example
- Status / Expectation

Include:
- Data Validation
- Duplicate Validation
- Point-in-Time Validation
- Target Leakage Validation
- Feature Validation
- Time-Based Validation
- Model Validation


5. ML Output Table

Use the sample account-level churn prediction output.

Columns should include:
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

Clearly label:
Illustrative Sample Output


6. Open Items / Pending Business Clarifications Table

Columns:
- Topic
- Current Position
- Pending Decision
- Owner, if known
- Status
- Comments


DOCUMENT STYLE
==============

Create a professional Word document.

Use:
- Title page
- Table of Contents
- Numbered sections
- Landscape orientation for wide requirement tables where useful
- Repeat header row across pages
- Clear table borders
- Consistent fonts
- Compact spacing
- Page numbers
- Header/footer
- Auto-fit columns where possible

Avoid long paragraphs.

The purpose is to make the FRS easy to scan and review.


IMPORTANT FINAL RULES
=====================

1. Do NOT modify the existing FRS.
2. Create a new Word document only.
3. Preserve all existing requirements and business decisions.
4. Do not invent missing source mappings or decisions.
5. Keep open items open.
6. Every main requirement should have an example.
7. Use table format as the primary presentation style.
8. Keep descriptions concise.
9. Use the existing FRS and Clarifications_Internal(1).xlsx as the source of truth.
10. Save the output as:

Tactical_ML_Churn_FRS_Table_Format.docx

The final deliverable must be a .docx Word file.
