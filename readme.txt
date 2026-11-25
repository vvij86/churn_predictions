SELECT
    fundID,
    dbCode,
    mtNumber,
    subFund,
    COALESCE(NULLIF(mtNumber, ''), subFund) AS sub_fund,
    fundName
FROM Edge.FundList
WHERE fundID IN (
    5896, 5651, 5888, 5890,
    5891, 5889, 6109
)
ORDER BY fundID;
