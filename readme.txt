WITH ExitAccounts AS (
    SELECT
        acs.accountID,
        acs.fundID,
        f.sub_fund,
        acs.memberSource,
        acs.exitDate,
        DATEFROMPARTS(
            YEAR(acs.exitDate),
            MONTH(acs.exitDate),
            1
        ) AS month_start,

        CASE
            WHEN f.sub_fund IN ('MT888', 'MT999')
                 AND acs.exitDate >= '2025-03-19'
            THEN 1
            WHEN acs.memberSource = 'PC1PSUPERB'
            THEN 1
            ELSE 0
        END AS IsTransitionedMemberExit

    FROM MercerEdge.Edge.AccountSummary acs

    LEFT JOIN MercerEdge.Edge.FundList f
        ON f.fundID = acs.fundID

    WHERE acs.exitType = 'Exit'
      AND acs.exitDate >= '2024-01-01'
      AND acs.exitDate < '2026-11-01'
)

SELECT
    month_start,

    COUNT(DISTINCT accountID)
        AS total_exit_accounts,

    COUNT(DISTINCT CASE
        WHEN IsTransitionedMemberExit = 1
        THEN accountID
    END) AS transitioned_exit_accounts,

    COUNT(DISTINCT CASE
        WHEN IsTransitionedMemberExit = 0
        THEN accountID
    END) AS non_transitioned_exit_accounts

FROM ExitAccounts
GROUP BY month_start
ORDER BY month_start;
