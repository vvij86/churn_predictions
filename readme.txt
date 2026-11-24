DECLARE @AsOfDate DATE = '2024-03-31';
DECLARE @OutcomeEndDate DATE = '2024-06-29';

-- Ground-truth churn validation
SELECT
    COUNT(DISTINCT a.account_id) AS churn_account_count
FROM AccountSummary a
WHERE
    a.exitDateRecorded > @AsOfDate
    AND a.exitDateRecorded <= @OutcomeEndDate

    -- Approved churn/full-exit types
    AND a.exitType IN (
        'Full Withdrawal',
        'Account Closure due to full exit',
        'Full Rollover Out'
    )

    -- Exclude deceased members
    AND a.dateOfDeath IS NULL

    -- Exclude internal transfers
    AND ISNULL(a.exitType, '') <> 'Internal Transfer'

    AND NOT EXISTS (
        SELECT 1
        FROM AccountRolloverPayment r
        WHERE r.account_id = a.account_id
          AND ISNULL(r.internalTransferFlag, 0) = 1
    );
