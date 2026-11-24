USE CATALOG mer_wealth_dev;
USE SCHEMA mer_wealth_landing_edge;

WITH exited_accounts AS (
    SELECT DISTINCT
        a.accountID
    FROM mscs_mrt_account_summary a
    WHERE a.exitDateRecorded > DATE '2024-03-31'
      AND a.exitDateRecorded <= DATE '2024-06-29'
      AND a.exitType = 'Exit'
      AND a.dateOfDeath IS NULL
),

internal_transfer_accounts AS (
    SELECT DISTINCT
        r.accountID
    FROM mscs_mrt_account_rollover_payment r
    WHERE COALESCE(r.internalTransferFlag, false) = true
)

SELECT
    COUNT(DISTINCT e.accountID) AS churn_account_count
FROM exited_accounts e
LEFT ANTI JOIN internal_transfer_accounts i
    ON e.accountID = i.accountID;
