==================================================
DOCUMENT CHANGE SUMMARY
==================================================

Add a dedicated section near the beginning of the document titled:

"Feature Review Change Summary"

This section must clearly show what changed compared with the previous
"Member Retention Behavioral Feature Business Review" document.

Create three tables:

1. Newly Added Features
2. Removed / De-scoped Features
3. Retained but Updated / Reviewed Features

For each table use these columns:

Feature Group
Feature Name
Change
Reason

Examples of Change values:
- NEW
- REMOVED
- DE-SCOPED
- RETAINED
- REVIEW
- RENAMED
- LOGIC UPDATED

For newly added features, explain briefly why they were added.

Examples:
- New percentage-based Partial Rollover feature
- New targeted AccountEngagementWeb intent feature
- New recency feature
- New change/cessation behavioural signal

For removed/de-scoped features, state the actual business-review reason such as:
- duplicate of another authoritative source
- generic / low-signal activity
- insufficient coverage
- amount does not represent engagement
- derived/redundant feature
- leakage risk
- replaced by a more specific behavioural feature

For retained but updated features, explain whether:
- calculation logic changed
- business interpretation changed
- source remained the same
- feature moved from generic activity to targeted intent
- feature remains under REVIEW

IMPORTANT:
Derive this change summary by comparing:
1. the previous Word document
2. behavioural_features_business_review.sql
3. AccountEngagementWeb_Reviewed_Features.sql

Do not guess changes from feature names alone.

==================================================
FONT AND TABLE FORMATTING - MANDATORY
==================================================

Use Calibri throughout the document.

IMPORTANT TABLE FONT REQUIREMENT:

All BODY DATA inside every table must use:

Font: Calibri
Font size: 6.5 pt

This 6.5 pt requirement applies to:
- Behaviour Name
- Description
- Sample Value
- Source
- Comments
- S.No
- change-summary table data

Do NOT use 7 pt, 8 pt, 9 pt or automatic Word table font sizing.

Explicitly set every table body cell to Calibri 6.5 pt.

Table header row may be slightly larger for readability:
Calibri 7 pt, Bold

Section headings and document title may retain the same sizes and formatting as the original document.

Maintain the same:
- column widths
- borders
- cell shading
- paragraph spacing
- alignment
- page margins
- section-title styling

as the existing Member Retention Behavioral Feature Business Review document.

Do not allow Word's default table style to override the 6.5 pt body font.

After generating the document, programmatically verify:
- all table body cells use Calibri 6.5 pt
- all table header cells use the intended header font
- no table body text has reverted to 8/9/10/11 pt

==================================================
FINAL DOCUMENT SUMMARY
==================================================

At the end of the document add:

"Final Feature Review Summary"

Include:

- Previous feature count
- Final active feature count
- Number of newly added features
- Number of removed / de-scoped features
- Number of REVIEW features
- Number of leakage-risk features removed
- Count by feature group

Also provide a short bullet list of the most important changes.

Examples:
- Generic Workflow behaviour de-scoped
- Duplicate Campaign contribution events removed
- Contribution change/cessation signals retained
- Duplicate Inflow raw current amounts removed
- Partial Rollover percentage features added
- Insurance amount fields de-scoped
- Generic AccountEngagementWeb metrics replaced with targeted digital-intent features
- ExitDate excluded due to leakage

Only state a change if it is supported by the reviewed SQL and previous document.
