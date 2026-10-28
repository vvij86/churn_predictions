Yes — then simplify the Copilot task. Ask it to keep only strong candidates and exclude anything uncertain instead of carrying REVIEW REQUIRED items forward.

Use this prompt:

Read the latest behavioural_features_business_review.sql, member_retention_ml_copilot_instructions.md, and inspect edgeSource.accountEngagementWorkflow.

I want to improve the workflow feature logic using jobDescription.

Business has already confirmed:

- Exclude RF-Processor
- Exclude SUPERFACTS / SUPERFACTSS
- Include Internet
- Include E-mail

However, jobDescription contains richer business meaning than jobSourceDescription.

Do not modify any files yet.

Objective

Identify only strong, clearly meaningful member-behaviour candidates from jobDescription that are suitable for churn prediction.

Do not keep uncertain or ambiguous items.

If the business meaning is unclear, treat it as:

EXCLUDE FOR NOW

instead of REVIEW REQUIRED.

Step 1 – Profile jobDescription

Analyze distinct combinations of:

- jobSourceDescription
- jobDescription

Include:

- row count
- distinct account count

Focus on high-frequency descriptions first, but also identify lower-frequency descriptions that clearly represent meaningful member behaviour.

Step 2 – Keep only strong candidates

Classify each relevant jobDescription as:

- INCLUDE
- EXCLUDE FOR NOW

INCLUDE only when the description clearly represents member behaviour such as:

- member inquiry/service request
- complaint/escalation
- member profile/contact-detail change
- beneficiary activity
- member-initiated insurance activity
- member-initiated investment activity
- member correspondence/contact
- advice-related activity

EXCLUDE FOR NOW when it is:

- ambiguous
- system-generated
- processor-generated
- batch activity
- reporting/reconciliation
- admin/back-office activity
- technical/error handling
- operational processing
- claim/death processing
- rollover/payment activity already covered by dedicated sources
- contribution activity already better represented by dedicated contribution tables
- potentially target-leaking
- too unclear to confidently interpret

Do not retain uncertain features just for completeness.

Step 3 – Group strong candidates

Do not create one feature per jobDescription.

Group only the strong included descriptions into a small number of categories such as:

- MEMBER_INQUIRY_SERVICE
- COMPLAINT_ESCALATION
- MEMBER_DETAIL_CHANGE
- BENEFICIARY_ACTIVITY
- INSURANCE_ACTIVITY
- INVESTMENT_ACTIVITY
- MEMBER_CORRESPONDENCE
- ADVICE_ACTIVITY

Create a group only when the actual data clearly supports it.

Step 4 – Avoid duplication

Check whether a workflow candidate duplicates a stronger dedicated source.

Examples:

- rollover/payment → prefer accountRolloverPayment
- contribution behaviour → prefer accountMoneyInflow / accountNetMoneyFlow
- investment behaviour → compare with accountInvestments
- insurance behaviour → compare with AccountInsuranceCurrent

If the dedicated source provides a clearer and more reliable signal, exclude the workflow version.

Step 5 – Output shortlist

Return a table:

S.No | jobSourceDescription | jobDescription / Pattern | Suggested Group | INCLUDE / EXCLUDE FOR NOW | Reason

Then provide a separate final list containing only:

Strong workflow candidates recommended for ML

Do not include ambiguous items in that final list.

Step 6 – Recommend final workflow features

From the strong candidates only, recommend a compact feature set such as:

- meaningful_workflow_count_12m
- recent_meaningful_workflow_count_90d
- recent_meaningful_workflow_count_30d
- days_since_last_meaningful_workflow
- meaningful_workflow_active_days_12m
- inquiry_service_count_12m
- complaint_escalation_count_12m
- recent_complaint_escalation_count_90d
- member_detail_change_count_12m
- beneficiary_workflow_count_12m

Only recommend features actually supported by the strong jobDescription candidates found in the data.

Important

- jobDescription should determine business meaning.
- jobSourceDescription should mainly indicate channel/source.
- Do not include a workflow just because its source is Internet or E-mail if the description is operational/admin.
- Do not exclude a strong member behaviour just because its source is Written Request or another channel.
- Avoid leakage.
- Avoid duplicate signals.
- Prefer fewer strong features over many uncertain ones.

Do not modify SQL or Word documents yet.

Stop after identifying and recommending the strong candidates.
