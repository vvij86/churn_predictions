%sql
SELECT
    as_of_date,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT account_id) AS distinct_accounts,
    COUNT(*) - COUNT(DISTINCT account_id)
        AS duplicate_or_null_keys
FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features
GROUP BY as_of_date
ORDER BY as_of_date;
