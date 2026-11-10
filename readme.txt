Update ONLY the Inflow Signals / Contribution Change section in behavioural_features_business_review.sql based on the completed live-data review.

Do not modify any other feature block.

Apply the following final decision:

DE-SCOPE these duplicate current/raw amount features from the active output:
1. employer_sg_current_amount_12m
2. salary_sacrifice_current_amount_12m
3. member_voluntary_current_amount_12m

Reason:
These are materially equivalent to the corresponding retained Contribution Behaviour amount features already calculated from edgeSource.accountMoneyInflow, using the same source rows, same eligible account population, same 12-month window, same contribution-type restrictions, same internal-transfer/rollover exclusions, and SUM(amount) aggregation.

KEEP these behavioural change features active:
1. employer_sg_change_pct_12m
2. employer_sg_cessation_flag
3. salary_sacrifice_change_pct_12m
4. salary_sacrifice_cessation_flag
5. member_voluntary_change_pct_12m
6. member_voluntary_cessation_flag

Reason:
- change_pct features measure within-account current-vs-prior contribution change
- cessation flags measure contribution stopping/deterioration
- these are not duplicate copies of the raw amount totals

Implementation requirements:
- Remove/comment out ONLY the 3 de-scoped current_amount fields from the final active SELECT/output.
- Preserve their calculation code as commented reference code with a short BUSINESS REVIEW note explaining why they were de-scoped.
- Do not change the formulas for the 6 retained features.
- Do not change contribution filtering, eligible-account logic, date windows, internal-transfer exclusions, rollover exclusions, or account-level grain.
- Do not touch Campaign/Event, Workflow, Helpline, Website, Partial Rollover, or any other section.

After the SQL change, validate the live output and return:

1. Active Inflow Signals / Contribution Change feature list.
2. Confirm these are NOT active:
   - employer_sg_current_amount_12m
   - salary_sacrifice_current_amount_12m
   - member_voluntary_current_amount_12m
3. Confirm all 6 retained change/cessation features ARE active.
4. post-AsOfDate rows entering feature logic = X
5. pre-FeatureStartDate rows entering feature logic = X
6. final duplicate accountID count = X
7. final grain = one row per accountID: YES/NO
8. PASS / FAIL

PASS only if:
- the 3 duplicate raw/current amount features are no longer active,
- all 6 behavioural change/cessation features remain active,
- post-AsOfDate rows = 0,
- pre-FeatureStartDate rows = 0,
- final duplicate accountID count = 0.

Also show exactly which SQL lines/features were changed.
