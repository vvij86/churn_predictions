WITH ExitAccounts AS
(
    SELECT DISTINCT
        accountID,
        fundID,
        CONVERT(VARCHAR(7), exitDateRecorded, 120) AS exit_month
    FROM Edge.AccountSummary
    WHERE databaseCode = 'ST000'
        AND exitType = 'Exit'
        AND exitDateRecorded >= '2026-03-01'
        AND exitDateRecorded < '2026-05-01'
),
PaymentAccounts AS
(
    SELECT DISTINCT
        accountID,
        CONVERT(VARCHAR(7), processedDate, 120) AS payment_month
    FROM Edge.AccountRolloverPayment
    WHERE processedDate >= '2026-03-01'
        AND processedDate < '2026-05-01'
)
SELECT
    a.exit_month,
    a.fundID,
    COUNT(DISTINCT a.accountID) AS total_exits,

    COUNT(DISTINCT CASE
        WHEN r.accountID IS NOT NULL
        THEN a.accountID
    END) AS exits_with_payment,

    COUNT(DISTINCT CASE
        WHEN r.accountID IS NULL
        THEN a.accountID
    END) AS exits_without_payment

FROM ExitAccounts a
LEFT JOIN PaymentAccounts r
    ON a.accountID = r.accountID
    AND a.exit_month = r.payment_month
GROUP BY
    a.exit_month,
    a.fundID
ORDER BY
    a.exit_month,
    total_exits DESC;
