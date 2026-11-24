DECLARE @AsOfDate DATE = '2024-03-31';
DECLARE @OutcomeEndDate DATE = '2024-06-29';

SELECT
    COUNT(DISTINCT a.accountID) AS churn_account_count
FROM Edge.AccountSummary a
WHERE a.exitDateRecorded > @AsOfDate
  AND a.exitDateRecorded <= @OutcomeEndDate
  AND a.exitType = 'Exit'
  AND a.dateOfDeath IS NULL
  AND NOT EXISTS (
      SELECT 1
      FROM Edge.AccountRolloverPayment r
      WHERE r.accountID = a.accountID
        AND ISNULL(r.internalTransferFlag, 0) = 1
  );
