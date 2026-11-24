SELECT COUNT(DISTINCT account_id)
FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth
WHERE as_of_date = DATE '2024-03-31'
  AND target_churn = 1;
