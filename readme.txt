%sql

SELECT
    MIN(as_of_date) AS first_snapshot,
    MAX(as_of_date) AS last_snapshot,
    COUNT(DISTINCT as_of_date) AS total_snapshots,
    COUNT(*) AS total_feature_rows,
    COUNT(DISTINCT account_id) AS unique_accounts,
    COUNT(DISTINCT STRUCT(account_id, as_of_date))
        AS distinct_key_rows,
    COUNT(*) -
        COUNT(DISTINCT STRUCT(account_id, as_of_date))
        AS duplicate_keys,
    COUNT_IF(account_id IS NULL OR as_of_date IS NULL)
        AS null_keys
FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features;
