USE CATALOG mer_wealth_dev;
USE SCHEMA mer_wealth_mra_mlops;

-- 1. Overall ground-truth dataset summary
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT as_of_date) AS snapshot_count,
    MIN(as_of_date) AS first_snapshot,
    MAX(as_of_date) AS last_snapshot
FROM member_retention_ground_truth;


-- 2. Row count and churn distribution by snapshot
SELECT
    as_of_date,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN target_churn = 1 THEN 1 ELSE 0 END) AS churn_rows,
    SUM(CASE WHEN target_churn = 0 THEN 1 ELSE 0 END) AS retained_rows,
    ROUND(
        100.0 * SUM(CASE WHEN target_churn = 1 THEN 1 ELSE 0 END) / COUNT(*),
        4
    ) AS churn_pct
FROM member_retention_ground_truth
GROUP BY as_of_date
ORDER BY as_of_date;


-- 3. Duplicate grain check - should return ZERO rows
SELECT
    account_id,
    as_of_date,
    COUNT(*) AS cnt
FROM member_retention_ground_truth
GROUP BY account_id, as_of_date
HAVING COUNT(*) > 1;


-- 4. Null / invalid target checks - all should be ZERO
SELECT
    SUM(CASE WHEN account_id IS NULL THEN 1 ELSE 0 END) AS null_account_id,
    SUM(CASE WHEN as_of_date IS NULL THEN 1 ELSE 0 END) AS null_as_of_date,
    SUM(CASE WHEN target_churn IS NULL THEN 1 ELSE 0 END) AS null_target,
    SUM(CASE WHEN target_churn NOT IN (0,1) THEN 1 ELSE 0 END) AS invalid_target
FROM member_retention_ground_truth;


-- 5. Feature table snapshot check
SELECT
    as_of_date,
    COUNT(*) AS feature_rows,
    COUNT(DISTINCT account_id) AS distinct_accounts
FROM member_retention_features
GROUP BY as_of_date
ORDER BY as_of_date;


-- 6. Feature vs ground-truth row-count comparison
SELECT
    f.as_of_date,
    f.feature_rows,
    g.ground_truth_rows,
    f.feature_rows - g.ground_truth_rows AS difference
FROM (
    SELECT as_of_date, COUNT(*) AS feature_rows
    FROM member_retention_features
    GROUP BY as_of_date
) f
JOIN (
    SELECT as_of_date, COUNT(*) AS ground_truth_rows
    FROM member_retention_ground_truth
    GROUP BY as_of_date
) g
ON f.as_of_date = g.as_of_date
ORDER BY f.as_of_date;
