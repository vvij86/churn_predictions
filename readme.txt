Create a NEW Word document for the final reviewed behavioural feature list.

IMPORTANT:
Do NOT overwrite the existing document:
"Member Retention Behavioral Feature Business Review"

Create a new document, for example:

Member_Retention_Behavioural_Features_Final_Reviewed.docx

Use the SAME formatting, structure, table style, fonts, section headings, column widths, borders, shading and overall layout as the existing:
"Member Retention Behavioral Feature Business Review"

The existing document should be used only as the formatting/template reference.

==================================================
SOURCE OF TRUTH
==================================================

The final active feature definitions must come from these two SQL files:

1. behavioural_features_business_review.sql
2. AccountEngagementWeb_Reviewed_Features.sql

Do NOT use the old Word document as the source of truth for feature inclusion.

The Word document must represent the CURRENT reviewed SQL state.

Where a feature has been commented out / de-scoped / removed from active SELECT output in SQL, do NOT include it as an active feature.

Where a feature is explicitly retained in SQL, include it.

For AccountEngagementWeb, use the standalone:
AccountEngagementWeb_Reviewed_Features.sql

because AccountEngagementWeb was reviewed separately using the production XLSX files.

==================================================
DOCUMENT PURPOSE
==================================================

Create a clean final business-review feature catalogue containing the latest scoped behavioural features that are candidates for the ML model.

The document must be understandable by:
- Business
- BA
- Data Science
- ML reviewers

Do not include temporary validation columns, debug outputs, intermediate CTE fields, or technical helper columns.

==================================================
DOCUMENT STRUCTURE
==================================================

Retain the same section-based format used in the existing Word document.

For each feature group, create a table with exactly these columns:

S.No
Behaviour Name
Description
Sample Value
Source
Comments

Use the same styling as the existing document.

Number rows sequentially within each section.

==================================================
FEATURE INCLUSION RULES
==================================================

Read the SQL carefully and generate the final active feature list.

Do NOT simply copy all historical rows from the old Word document.

Include only currently retained / active fields.

==================================================
1. HELPLINE ENGAGEMENT
==================================================

Use the final reviewed Helpline logic from behavioural_features_business_review.sql.

Do not reintroduce fields already de-scoped during review.

Preserve only active Helpline behavioural features.

For complaint-related fields:
respect the earlier business review warning that Helpline complaints capture only a narrow subset of complaints.

Do not promote a complaint feature if it has been de-scoped in the reviewed SQL.

==================================================
2. WORKFLOW BEHAVIOUR
==================================================

The Workflow review concluded that the generic workflow features and category-specific weak signals were not strong enough.

Do NOT include de-scoped Workflow fields merely because the SQL reference code still exists.

If the final active SQL output contains no Workflow ML features, either:

- omit the Workflow section entirely

OR

- retain a short section heading with a note:
  "De-scoped during business review — no active ML features retained."

Prefer omitting individual de-scoped rows.

==================================================
3. CONTRIBUTION BEHAVIOUR
==================================================

Include the currently retained Contribution Behaviour features from behavioural_features_business_review.sql.

These may include features such as:

- contribution_count_12m
- contribution_amount_12m
- contribution_active_months_12m
- days_since_last_contribution
- recent_contribution_amount_90d
- prior_contribution_amount_90d
- recent_contribution_count_90d
- prior_contribution_count_90d
- contribution_change_pct_90d
- contribution_ceased_90d_flag
- employer_sg_amount_12m
- employer_sg_amount_90d
- salary_sacrifice_amount_12m
- salary_sacrifice_amount_90d
- member_voluntary_amount_12m
- member_voluntary_amount_90d

BUT verify against the current SQL before including.

Important business wording:

Raw contribution monetary values are financial-behaviour measures.

Do NOT describe larger contribution amount as stronger engagement.

Frequency, persistence, recency, relative change and cessation are stronger behavioural signals.

==================================================
4. CAMPAIGN / EVENT CONTRIBUTION DEDUPLICATION
==================================================

Do NOT include:

- contribution_event_count_12m
- recent_contribution_event_count_90d

because these were de-scoped as possible duplicates of accountMoneyInflow contribution behaviour.

Retain roll-in event fields only if they remain active in the final SQL.

For example, verify whether the following are active:

- rollin_event_count_12m
- recent_rollin_event_count_90d

If retained, mention in Comments that these are still under review as transfer-in / roll-in signals and are not treated as duplicates of normal contributions.

==================================================
5. INFLOW SIGNALS / CONTRIBUTION CHANGE
==================================================

Do not include duplicate raw/current amount fields that were de-scoped.

Specifically verify and exclude the de-scoped current amount features such as:

- employer_sg_current_amount_12m
- salary_sacrifice_current_amount_12m
- member_voluntary_current_amount_12m

Retain behavioural change / cessation features if active, such as:

- employer_sg_change_pct_12m
- employer_sg_cessation_flag
- salary_sacrifice_change_pct_12m
- salary_sacrifice_cessation_flag
- member_voluntary_change_pct_12m
- member_voluntary_cessation_flag

Verify exact active column names from the SQL.

==================================================
6. PARTIAL ROLLOVER / WITHDRAWAL BEHAVIOUR
==================================================

Include the final reviewed Partial Rollover features.

Expected active features should be verified from SQL and may include:

- partial_rollover_count_12m
- partial_rollover_amount_12m
- days_since_last_partial_rollover
- recent_partial_rollover_count_90d
- recent_partial_rollover_amount_90d
- partial_rollover_pct_12m
- recent_partial_rollover_pct_90d

Also include current_account_fum_amount only if it is an intended active feature in the final modelling output.

Important description for percentage features:

partial_rollover_pct_12m represents the proportion of the account's pre-withdrawal value represented by partial rollover activity.

The final reviewed denominator logic is:

partial_rollover_amount_12m /
(current_account_fum_amount + partial_rollover_amount_12m)

and similarly for the recent 90-day percentage.

Only positive FUM is used for percentage calculation.

Do not show implementation SQL in the document; convert it to simple business wording.

==================================================
7. INVESTMENT BEHAVIOUR / POSITION
==================================================

Use the final active features from AccountInvestments.

Verify against SQL.

Potential fields include:
- investment_option_count_asof
- total_investment_value_asof
- direct_investment_flag

Do not invent new features.

If total_investment_value_asof is effectively the account-level FUM used elsewhere, describe it consistently and avoid duplicate naming if the final SQL has one canonical field.

==================================================
8. INSURANCE BEHAVIOUR / COVER POSITION
==================================================

Use the latest review decision.

KEEP:
- has_death_cover_asof
- has_tpd_cover_asof

The review indicated that the amount fields were not useful behavioural signals.

Do NOT include if de-scoped:
- death_cover_amount_asof
- tpd_cover_amount_asof
- ip_cover_amount_asof

For:
- has_ip_cover_asof
- insurance_cover_type_count_asof

check the current SQL.

If still active but under review, include them with a clear Comments value such as:
"Retained for review — lower-prevalence / derived cover-position indicator."

Do not describe insurance amounts as engagement.

==================================================
9. ACCOUNT ENGAGEMENT WEB
==================================================

Use:
AccountEngagementWeb_Reviewed_Features.sql

Do NOT use the old generic AccountEngagementWeb feature list.

The reviewed production sample established that generic WebQuoteSummary activity is too broad.

Include only final scoped web behavioural-intent fields.

Expected retained/reviewed features to verify from the SQL:

Retirement planning:
- retirement_planning_activity_count_12m
- recent_retirement_planning_activity_count_90d
- days_since_last_retirement_planning_activity

Leaving-service quote intent:
- leaving_service_quote_count_12m
- recent_leaving_service_quote_count_90d
- days_since_last_leaving_service_quote

Transfer intent:
- transfer_intent_activity_count_12m
- recent_transfer_intent_activity_count_90d
- days_since_last_transfer_intent_activity

Investment switch:
- investment_switch_activity_count_12m
- recent_investment_switch_activity_count_90d
- days_since_last_investment_switch_activity

Verify exact final output columns from the standalone SQL.

Do NOT include generic web features such as:
- web_activity_count_12m
- web_active_days_12m
- days_since_last_web_activity
- recent_web_activity_count_90d

Do NOT use ExitDate.

Do NOT include any future exit/outcome parameter.

Do NOT include CurrentBalance or static financial values extracted from requestParameters.

Do NOT include generic WebQuoteSummary counts.

For source, use:
Edge.accountEngagementWeb
or the exact source naming convention used in the existing document.

For Comments:

Retirement planning:
"Retained — strongest genuine pre-churn digital intent observed in production sample."

Leaving-service:
"Retained / review — targeted leaving-service quote intent; generic WebQuoteSummary excluded."

Transfer intent:
"Retained / review — explicit member-initiated transfer intent."

Investment switch:
"Retained / review — explicit investment-change action."

==================================================
10. OTHER FEATURE GROUPS
==================================================

Continue through every feature section present in behavioural_features_business_review.sql.

Examples may include:
- Third Party Authority
- Member service
- Campaign
- FUM
- Investment
- other behavioural sections already implemented

For every section:

1. inspect current SQL
2. identify active final output features
3. exclude commented-out / de-scoped fields
4. preserve exact column name
5. write concise business description
6. use correct source table
7. add business-review comment only where needed

Do not lose any active reviewed feature simply because it was not explicitly mentioned in this prompt.

==================================================
SAMPLE VALUE RULES
==================================================

Match the style of the original document.

Examples:

Counts:
3

Flags:
1 (Yes)

Days-since:
15 days

Monetary:
$2,500.00

Percentage:
12.5%

Do not derive fake production-specific values.

These are illustrative sample values only, consistent with the existing document style.

==================================================
COMMENTS RULE
==================================================

Comments should capture only useful business-review context.

Examples:

- "Retained — strong recency signal."
- "Retained as financial behaviour; amount should not be interpreted as engagement strength."
- "Retained / review — possible overlap with another feature group."
- "Derived current-position indicator."
- "Production web review confirmed targeted intent; generic web activity excluded."

Do NOT add verbose technical SQL explanations inside Comments.

==================================================
FINAL QUALITY CHECK
==================================================

Before creating the document, produce an internal comparison of:

A. all active feature columns from behavioural_features_business_review.sql
B. all active feature columns from AccountEngagementWeb_Reviewed_Features.sql
C. all feature rows planned for the new Word document

Verify:

- no active SQL feature is accidentally omitted
- no de-scoped feature is accidentally included
- no duplicate feature appears in two sections unless there is a genuine business reason
- exact feature names match SQL
- source table is correct
- AccountEngagementWeb comes only from the reviewed standalone SQL
- ExitDate and other leakage fields are absent
- final modelling grain remains account level

==================================================
OUTPUT
==================================================

Create:

Member_Retention_Behavioural_Features_Final_Reviewed.docx

Use the SAME visual style as the existing:
Member Retention Behavioral Feature Business Review

At the end, also provide a short summary:

- total number of active features in the document
- count by feature group
- features removed/de-scoped compared with the old document
- newly added features compared with the old document
- features retained as REVIEW rather than fully KEEP

Do not modify either SQL file during this task.
Do not modify the existing Word document.
Only generate the new final reviewed Word document.
