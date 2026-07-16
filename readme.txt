SELECT
    account_closed_outcome_flag,
    outcome_external_rollover_flag,
    target_churn,
    COUNT(*) AS account_count
FROM final_output
WHERE exclude_from_training_flag = 0
GROUP BY
    account_closed_outcome_flag,
    outcome_external_rollover_flag,
    target_churn
ORDER BY
    target_churn,
    account_closed_outcome_flag,
    outcome_external_rollover_flag;
