DECLARE @AsOfDate DATE = '2024-03-31';
DECLARE @OutcomeEndDate DATE = '2024-06-29';

SELECT
    COUNT(DISTINCT a.accountID) AS churn_account_count
FROM Edge.AccountSummary a
WHERE
    CAST(a.exitDateRecorded AS DATE) > @AsOfDate
    AND CAST(a.exitDateRecorded AS DATE) <= @OutcomeEndDate

    AND a.databaseCode IN
    (
        'MASTA',
        'MASTP',
        'MASTR',
        'MASTS',
        'MASTM',
        'MTAPD',
        'ST000',
        'MASTR_AP'
    )

    AND LOWER(LTRIM(RTRIM(ISNULL(a.exitType, '')))) = 'exit'

    AND a.dateOfDeath IS NULL

    -- Exclude internal transfers
    AND NOT EXISTS
    (
        SELECT 1
        FROM Edge.AccountRolloverPayment r
        WHERE r.accountID = a.accountID
        AND ISNULL(r.internalTransferFlag, 0) = 1
    )

    -- Additional filter 1: Account joining date
    AND CAST(a.fundJoinDate AS DATE) <= @AsOfDate

    -- Additional filter 2: Death indicator
    AND ISNULL(CAST(a.deathIndicatorFlag AS INT), 0) = 0

    -- Additional filter 3: Valid reporting date
    AND a.reportingDate IS NOT NULL;
