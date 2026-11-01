Update "consolidated_behavioural_feature_dataset_review.sql" based on the validation result.

Restore only the genuinely missing validated standalone features from "behavioural_features_business_review.sql":

- days_since_last_investment_switch
- investment_switch_count_12m
- recent_investment_switch_count_90d
- employer_sg_current_amount_12m
- employer_sg_change_pct_12m
- employer_sg_cessation_flag
- salary_sacrifice_current_amount_12m
- salary_sacrifice_change_pct_12m
- salary_sacrifice_cessation_flag
- member_voluntary_current_amount_12m
- member_voluntary_change_pct_12m
- member_voluntary_cessation_flag

Do not add "total_investment_value_asof" separately. Keep "current_account_fum_amount" as the renamed business output for that same validated FUM calculation.

Do not modify any other feature logic, eligibility rules, AsOfDate logic, joins, leakage exclusions, or NULL handling.

After updating, validate again against "behavioural_features_business_review.sql" and report PASS/FAIL, missing features, extra features, final feature count, grain, duplicate-risk joins, point-in-time safety and leakage checks.
