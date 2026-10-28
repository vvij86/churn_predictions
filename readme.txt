-- 1. What insurance cover types exist?
SELECT DISTINCT
    coverDescription
FROM edgeSource.AccountInsuranceCurrent
ORDER BY coverDescription;

-- 2. What risk events exist?
SELECT DISTINCT
    riskEvent
FROM edgeSource.AccountInsuranceCurrent
ORDER BY riskEvent;

-- 3. What insurance types exist?
SELECT DISTINCT
    insuranceType
FROM edgeSource.AccountInsuranceCurrent
ORDER BY insuranceType;

-- 4. Check historical date availability
SELECT
    MIN(effectiveDateFrom) AS min_effective_date,
    MAX(effectiveDateFrom) AS max_effective_date,
    MIN(effectiveDateTo)   AS min_effective_to,
    MAX(effectiveDateTo)   AS max_effective_to,
    COUNT(*)               AS row_count
FROM edgeSource.AccountInsuranceCurrent;


SELECT
    coverDescription,
    riskEvent,
    COUNT(*) AS row_count,
    COUNT(DISTINCT accountID) AS account_count
FROM edgeSource.AccountInsuranceCurrent
GROUP BY
    coverDescription,
    riskEvent
ORDER BY row_count DESC;
