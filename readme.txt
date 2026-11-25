SELECT
    a.fundID,
    r.paymentType,
    r.rolloverInstitution,
    r.rolloverDestinationType,
    r.rolloverCode,
    COUNT(DISTINCT a.accountID) AS account_count
FROM Edge.AccountSummary a
INNER JOIN Edge.AccountRolloverPayment r
    ON a.accountID = r.accountID
WHERE a.databaseCode = 'ST000'
    AND a.exitType = 'Exit'
    AND a.exitDateRecorded >= '2026-03-01'
    AND a.exitDateRecorded < '2026-05-01'
    AND r.processedDate >= '2026-03-01'
    AND r.processedDate < '2026-05-01'
GROUP BY
    a.fundID,
    r.paymentType,
    r.rolloverInstitution,
    r.rolloverDestinationType,
    r.rolloverCode
ORDER BY account_count DESC;
