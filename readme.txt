%sql

SELECT
    as_of_date,
    COUNT(*) AS row_count,
    COUNT(DISTINCT account_id) AS distinct_accounts,
    COUNT(*) - COUNT(DISTINCT account_id)
        AS duplicate_or_null_keys
FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features
WHERE as_of_date = DATE '2024-03-31'
GROUP BY as_of_date;
