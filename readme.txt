Review `notebook/ml_mscs_mrt_contribution_features.py` against the reviewed Inflow Signals / Contribution Change logic in:

`behavioural_features_business_review.sql`

Follow `.github/copilot-instructions.md` strictly.

Do not modify code yet.

Check whether all 6 reviewed features are already implemented correctly:

- employer_sg_change_pct_12m
- employer_sg_cessation_flag
- salary_sacrifice_change_pct_12m
- salary_sacrifice_cessation_flag
- member_voluntary_change_pct_12m
- member_voluntary_cessation_flag

For each feature, report:

1. Present or missing.
2. Exact calculation currently used.
3. Whether it matches the reviewed SQL business logic.
4. Whether it uses the controlled as_of_date = 2024-03-31 correctly.
5. Whether any future data can enter the calculation.
6. Whether the feature is present in the final `contribution_features_df`.

Also confirm that the previously de-scoped duplicate current amount features are NOT included in the final output:

- employer_sg_current_amount_12m
- salary_sacrifice_current_amount_12m
- member_voluntary_current_amount_12m

Do not make any code changes until you provide the comparison result.
