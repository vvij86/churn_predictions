SELECT
    as_of_date,
    COUNT(*) AS total_accounts,
    SUM(CASE WHEN target_churn = 1 THEN 1 ELSE 0 END) AS churn_count,
    SUM(CASE WHEN target_churn = 0 THEN 1 ELSE 0 END) AS retained_count,
    ROUND(
        100.0 * SUM(CASE WHEN target_churn = 1 THEN 1 ELSE 0 END)
        / COUNT(*), 4
    ) AS churn_pct
FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth
WHERE as_of_date >= '2025-01-01'
GROUP BY as_of_date
ORDER BY as_of_date;
