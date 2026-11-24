USE CATALOG mer_wealth_dev;
USE SCHEMA mer_wealth_mra_mlops;

-- 1. Feature table row count by snapshot
SELECT
    as_of_date,
    COUNT(*) AS row_count,
    COUNT(DISTINCT account_id) AS distinct_accounts
FROM member_retention_features
GROUP BY as_of_date
ORDER BY as_of_date;

-- 2. Check duplicate keys in feature table
SELECT
    account_id,
    as_of_date,
    COUNT(*) AS duplicate_count
FROM member_retention_features
GROUP BY account_id, as_of_date
HAVING COUNT(*) > 1;

-- 3. Ground-truth row count + churn distribution
SELECT
    as_of_date,
    COUNT(*) AS row_count,
    SUM(CASE WHEN target_churn = 1 THEN 1 ELSE 0 END) AS churn_rows,
    SUM(CASE WHEN target_churn = 0 THEN 1 ELSE 0 END) AS retained_rows,
    ROUND(
        100.0 * SUM(CASE WHEN target_churn = 1 THEN 1 ELSE 0 END) / COUNT(*),
        4
    ) AS churn_pct
FROM member_retention_ground_truth
GROUP BY as_of_date
ORDER BY as_of_date;

-- 4. Check duplicate keys in ground-truth table
SELECT
    account_id,
    as_of_date,
    COUNT(*) AS duplicate_count
FROM member_retention_ground_truth
GROUP BY account_id, as_of_date
HAVING COUNT(*) > 1;

-- 5. Check null / invalid targets
SELECT
    SUM(CASE WHEN account_id IS NULL THEN 1 ELSE 0 END) AS null_account_id,
    SUM(CASE WHEN as_of_date IS NULL THEN 1 ELSE 0 END) AS null_as_of_date,
    SUM(CASE WHEN target_churn IS NULL THEN 1 ELSE 0 END) AS null_target,
    SUM(CASE WHEN target_churn NOT IN (0,1) THEN 1 ELSE 0 END) AS invalid_target
FROM member_retention_ground_truth;

-- 6. Total distinct snapshots
SELECT
    COUNT(DISTINCT as_of_date) AS snapshot_count
FROM member_retention_ground_truth;
