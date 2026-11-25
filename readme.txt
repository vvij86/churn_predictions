%sql

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT account_id, as_of_date) AS distinct_keys,
    COUNT(*) - COUNT(DISTINCT account_id, as_of_date)
        AS duplicate_rows
FROM account_profile_features_under_test;
