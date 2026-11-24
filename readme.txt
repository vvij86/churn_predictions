USE CATALOG mer_wealth_dev;

WITH eligible_accounts AS (
    SELECT DISTINCT account_id
    FROM mer_wealth_mra_mlops.member_retention_features
    WHERE as_of_date = DATE '2024-03-31'
),

exited_accounts AS (
    SELECT DISTINCT a.accountID
    FROM mer_wealth_landing_edge.mscs_mrt_account_summary a
    WHERE a.exitDateRecorded > DATE '2024-03-31'
      AND a.exitDateRecorded <= DATE '2024-06-29'
      AND a.exitType = 'Exit'
      AND a.dateOfDeath IS NULL
),

internal_transfer_accounts AS (
    SELECT DISTINCT r.accountID
    FROM mer_wealth_landing_edge.mscs_mrt_account_rollover_payment r
    WHERE COALESCE(r.internalTransferFlag, false) = true
)

SELECT
    COUNT(DISTINCT e.accountID) AS eligible_churn_account_count
FROM exited_accounts e
INNER JOIN eligible_accounts b
    ON e.accountID = b.account_id
LEFT ANTI JOIN internal_transfer_accounts i
    ON e.accountID = i.accountID;
