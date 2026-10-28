SELECT DISTINCT
    thirdPartyAuthorityType
FROM edgeSource.thirdPartyAuthority
ORDER BY thirdPartyAuthorityType;

SELECT
    thirdPartyAuthorityType,
    COUNT(*) AS row_count,
    COUNT(DISTINCT accountID) AS account_count
FROM edgeSource.thirdPartyAuthority
GROUP BY thirdPartyAuthorityType
ORDER BY row_count DESC;

SELECT
    MIN(dateAuthorityRequested) AS min_request_date,
    MAX(dateAuthorityRequested) AS max_request_date,
    MIN(terminationDate) AS min_termination_date,
    MAX(terminationDate) AS max_termination_date
FROM edgeSource.thirdPartyAuthority;
