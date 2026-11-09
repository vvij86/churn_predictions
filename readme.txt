Update only the Campaign / Event Behaviour section in "behavioural_features_business_review.sql".

Use the live-validation findings already completed. Do not modify any other feature section.

Apply the following changes conservatively.

1. De-scope generic campaign activity features

The following broad activity features were confirmed as high-volume but low-specificity:

- campaign_event_count_12m
- distinct_campaign_event_type_count_12m
- days_since_last_campaign_event
- recent_campaign_event_count_90d

Do not delete their SQL permanently.

Comment them out from the active feature output and add:

"-- BUSINESS REVIEW: candidate for removal - generic campaign activity is high coverage but low specificity and does not identify a meaningful retention-related behaviour."

Keep the underlying source logic available for reference.

2. ADVICE campaign features

Current live validation found zero Campaign/Event ADVICE records in the eligible 12-month window.

Do not delete the ADVICE mapping.

Keep the source mapping available but comment out the following features from the active ML feature output for now:

- advice_event_count_12m
- recent_advice_event_count_90d
- days_since_last_advice_event

Add:

"-- BUSINESS REVIEW: current UAT/source window has zero Campaign ADVICE coverage. Preserve mapping for future production/source validation; do not rely on as active ML feature yet."

Do not change the already-reviewed Helpline ADVICE logic.

3. WEBSITE_LOGIN features

Current live validation found zero WEBSITE_LOGIN rows in the eligible period.

Preserve the WEBSITE_LOGIN event mapping, but comment out from the active ML feature output:

- website_login_count_12m
- website_login_count_90d
- website_login_count_30d
- days_since_last_website_login

Add:

"-- BUSINESS REVIEW: WEBSITE_LOGIN currently has zero source coverage in this environment. Preserve logic for future production validation."

Do not confuse this with "accountEngagementWeb".

4. MEMBER_SERVICE

Live validation found only 7 accounts, mainly CONTACT_UPDATE, and no HELP_DESK_CALL records.

Comment out:

- member_service_event_count_12m
- recent_member_service_event_count_90d

from the active ML output.

Add:

"-- BUSINESS REVIEW: MEMBER_SERVICE is extremely sparse and current mapping is dominated by CONTACT_UPDATE rather than a clear member-service behavioural signal."

Preserve the source mapping for reference.

5. CONTRIBUTION events

Keep:

- contribution_event_count_12m
- recent_contribution_event_count_90d

Do not remove them.

Add a comment that live validation showed material overlap with MoneyInflow contribution activity, so they should be interpreted as event-based behavioural evidence rather than an independent financial signal.

Do not modify the MoneyInflow feature block.

6. ROLLIN

Keep:

- rollin_event_count_12m
- recent_rollin_event_count_90d

Preserve the current ROLLIN event mapping.

Add a comment noting possible overlap with contribution/transfer behaviour but retain it because it is a meaningful explicit event signal.

7. RETIREMENT / PENSION events

Keep:

- retirement_pension_event_count_12m
- recent_retirement_pension_event_count_90d

Use the actual source values already validated:

- PENSION
- ALLOCATED_PENSION
- TTR

Add:

"-- BUSINESS REVIEW: represents pension/product action events, including Pension Creation/TTR activity; do not describe generically as retirement inquiry intent."

Do not merge these with Helpline RETIREMENT_INQUIRY or SUPER_TO_PENSION_TTR.

8. INSURANCE

Keep:

- insurance_opt_in_12m_flag

Preserve the validated "INSURANCE_OPT_IN" mapping.

9. BENEFICIARY

Before using the beneficiary feature, normalize the source eventName mapping for known formatting variations of:

- NOMINATED_BENEFICIARY
- NOMINATED_BINDING_BENEFICIARY

Use trimming/normalization where appropriate rather than depending on an accidental leading/trailing space.

Keep:

- beneficiary_event_count_12m

After the normalization, validate account coverage again.

10. INVESTMENT SWITCH

Keep the existing INVESTMENT_CHANGE / investment-switch feature logic.

Add a business-review comment stating that it represents an investment-switch/product action and should be treated as a specific behavioural signal rather than generic campaign activity.

Validation after the change

Run live database validation and report:

1. duplicate accountID rows in the final Campaign aggregation
2. source rows after @AsOfDate
3. active feature list after the changes
4. account coverage for every retained Campaign/Event feature
5. confirm generic campaign, ADVICE, WEBSITE_LOGIN and MEMBER_SERVICE features are no longer in the active feature output
6. confirm CONTRIBUTION, ROLLIN, RETIREMENT/PENSION, INSURANCE, BENEFICIARY and INVESTMENT SWITCH remain active
7. confirm beneficiary normalization captures all intended source variants

Do not change the consolidated dataset SQL yet.

Return a short PASS / REVIEW / FAIL summary and show exactly which lines/features were changed.
