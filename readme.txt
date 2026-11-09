Update only the Helpline section in "behavioural_features_business_review.sql".

Do not modify any other feature block.

There is an obsolete duplicate Consolidation/Rollover CASE branch still present in the query.

Keep this new live-data-validated logic:

-- BUSINESS REVIEW CHANGE - LIVE DATA VALIDATED
WHEN h.inquiryDescription = 'Consolidation Outbound'
  OR h.inquiryDescription = 'Choice/Consolidate Super'
  OR h.inquiryDescription LIKE '%Roll out%'
THEN 'ROLLOVER_CONSOLIDATION_INTENT'

Remove or comment out the old Consolidation/Rollover branch that contains:

WHEN h.inquiryDescription IN
(
    'Consolidation Inbound',
    'Consolidation Outbound'
)
OR h.inquiryDescription LIKE 'Choice/Consolidate%'
THEN 'CONSOLIDATION_ROLLOVER'

Reason:

- "Consolidation Inbound" must not be treated as churn/exit intent.
- The broad "Choice/Consolidate%" rule has already been replaced by the stricter live-data-validated rule.
- We must avoid two different categories representing the same rollover concept.

After the change, confirm there is only one active rollover/consolidation intent rule in the Helpline CASE logic.

Do not change:

- RESOLVED logic
- Super-to-Pension/TTR logic
- Retirement Inquiry logic
- Advice
- Contribution
- Investment
- Insurance
- Digital Access
- Complaint
- Account Admin
- Campaign logic
- date-window logic
- account-level aggregation

Also review the variable declarations.

If the validation section declares "@AsOfDate", "@FeatureStartDate", "@Recent90Start", or "@Recent30Start" again in the same SQL batch, ensure this will not cause duplicate variable declaration errors.

Either:

- separate the validation section using "GO", if appropriate for this standalone SQL file,
  or
- rename the validation-only variables.

Do not change the actual AsOfDate value or feature-window calculations.

Then run the live validation using the existing DB connection pattern and confirm:

1. "Consolidation Inbound" captured as rollover intent = 0.
2. "Choice of Fund" captured as rollover intent = 0.
3. "Investment Choice - change" captured as rollover intent = 0.
4. "Investment Choice advice" captured as rollover intent = 0.
5. "MST good choices" captured as rollover intent = 0.
6. Duplicate "accountID" count in final Helpline aggregation = 0.
7. Source records after "@AsOfDate" = 0.
8. There is only one active rollover/consolidation category name:
   "ROLLOVER_CONSOLIDATION_INTENT".

Do not broaden the rule and do not reintroduce generic "%Choice%" or "%Consolidat%".

At the end, show:

- what duplicate logic was removed
- the final active rollover rule
- PASS / REVIEW / FAIL validation result
