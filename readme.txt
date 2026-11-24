WITH raw_churn AS (
    SELECT DISTINCT a.accountID AS account_id
    FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary a

    INNER JOIN (
        SELECT DISTINCT account_id
        FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features
        WHERE as_of_date = DATE '2024-03-31'
    ) b
        ON a.accountID = b.account_id

    LEFT ANTI JOIN (
        SELECT DISTINCT accountID
        FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_rollover_payment
        WHERE COALESCE(internalTransferFlag, false) = true
    ) i
        ON a.accountID = i.accountID

    WHERE a.exitDateRecorded > DATE '2024-03-31'
      AND a.exitDateRecorded <= DATE '2024-06-29'
      AND a.exitType = 'Exit'
      AND a.dateOfDeath IS NULL
),

gt AS (
    SELECT DISTINCT account_id
    FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_ground_truth
    WHERE as_of_date = DATE '2024-03-31'
      AND target_churn = 1
)

SELECT
    'RAW_NOT_GT' AS mismatch_type,
    COUNT(*) AS account_count
FROM raw_churn r
LEFT ANTI JOIN gt g
    ON r.account_id = g.account_id

UNION ALL

SELECT
    'GT_NOT_RAW' AS mismatch_type,
    COUNT(*) AS account_count
FROM gt g
LEFT ANTI JOIN raw_churn r
    ON g.account_id = r.account_id;
