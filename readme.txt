%sql

SELECT
    as_of_date,
    outcome_horizon_key,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT account_id) AS unique_accounts,
    COUNT_IF(target_churn = 1) AS churn_count,
    COUNT_IF(target_churn = 0) AS non_churn_count,
    COUNT_IF(target_churn IS NULL) AS null_targets
FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth_6m
GROUP BY as_of_date, outcome_horizon_key;
