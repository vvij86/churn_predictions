SELECT
    a.fundID,
    f.fundName,
    CONVERT(VARCHAR(7), a.exitDateRecorded, 120) AS exit_month,
    r.paymentType,
    COUNT(DISTINCT a.accountID) AS account_count
FROM Edge.AccountSummary a
INNER JOIN Edge.AccountRolloverPayment r
    ON a.accountID = r.accountID
INNER JOIN Edge.FundList f
    ON a.fundID = f.fundID
WHERE a.databaseCode = 'ST000'
    AND a.exitType = 'Exit'
    AND a.exitDateRecorded >= '2026-03-01'
    AND a.exitDateRecorded < '2026-05-01'
    AND CONVERT(VARCHAR(7), a.exitDateRecorded, 120)
        = CONVERT(VARCHAR(7), r.processedDate, 120)
GROUP BY
    a.fundID,
    f.fundName,
    CONVERT(VARCHAR(7), a.exitDateRecorded, 120),
    r.paymentType
ORDER BY account_count DESC;
