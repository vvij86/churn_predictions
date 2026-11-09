/* ============================================================
   POINT 2 + POINT 3 HELPLINE VALIDATION
   Source: edgeSource.accountEngagementHelpline
   ============================================================ */

DECLARE @AsOfDate DATE = '2024-12-31';
DECLARE @FeatureStartDate DATE =
    DATEADD(DAY, 1, DATEADD(MONTH, -12, @AsOfDate));


/* ============================================================
   POINT 2
   Super to Pension / TTR
   Check actual Outcome + Inquiry descriptions
   ============================================================ */

SELECT
    outcomeDescription,
    inquiryDescription,
    COUNT(*) AS record_count,
    COUNT(DISTINCT accountID) AS account_count
FROM edgeSource.accountEngagementHelpline
WHERE callDate >= @FeatureStartDate
  AND callDate <= @AsOfDate
  AND
  (
       outcomeDescription LIKE '%Super to Pension%'
    OR inquiryDescription LIKE '%Super to Pension%'
    OR outcomeDescription LIKE '%TTR%'
    OR inquiryDescription LIKE '%TTR%'
  )
GROUP BY
    outcomeDescription,
    inquiryDescription
ORDER BY record_count DESC;


/* ============================================================
   POINT 2 - SAMPLE RAW RECORDS
   ============================================================ */

SELECT TOP 50
    accountID,
    callDate,
    outcomeDescription,
    inquiryDescription
FROM edgeSource.accountEngagementHelpline
WHERE callDate >= @FeatureStartDate
  AND callDate <= @AsOfDate
  AND
  (
       outcomeDescription LIKE '%Super to Pension%'
    OR inquiryDescription LIKE '%Super to Pension%'
    OR outcomeDescription LIKE '%TTR%'
    OR inquiryDescription LIKE '%TTR%'
  )
ORDER BY callDate DESC;


/* ============================================================
   POINT 3
   Retirement inquiry
   Check actual Outcome + Inquiry descriptions
   ============================================================ */

SELECT
    outcomeDescription,
    inquiryDescription,
    COUNT(*) AS record_count,
    COUNT(DISTINCT accountID) AS account_count
FROM edgeSource.accountEngagementHelpline
WHERE callDate >= @FeatureStartDate
  AND callDate <= @AsOfDate
  AND
  (
       outcomeDescription LIKE '%Retirement%'
    OR inquiryDescription LIKE '%Retirement%'
  )
GROUP BY
    outcomeDescription,
    inquiryDescription
ORDER BY record_count DESC;


/* ============================================================
   POINT 3 - SAMPLE RAW RECORDS
   ============================================================ */

SELECT TOP 50
    accountID,
    callDate,
    outcomeDescription,
    inquiryDescription
FROM edgeSource.accountEngagementHelpline
WHERE callDate >= @FeatureStartDate
  AND callDate <= @AsOfDate
  AND
  (
       outcomeDescription LIKE '%Retirement%'
    OR inquiryDescription LIKE '%Retirement%'
  )
ORDER BY callDate DESC;


/* ============================================================
   OVERLAP CHECK
   Records matching BOTH Point 2 and Point 3
   ============================================================ */

SELECT TOP 100
    accountID,
    callDate,
    outcomeDescription,
    inquiryDescription
FROM edgeSource.accountEngagementHelpline
WHERE callDate >= @FeatureStartDate
  AND callDate <= @AsOfDate

  AND
  (
       outcomeDescription LIKE '%Super to Pension%'
    OR inquiryDescription LIKE '%Super to Pension%'
    OR outcomeDescription LIKE '%TTR%'
    OR inquiryDescription LIKE '%TTR%'
  )

  AND
  (
       outcomeDescription LIKE '%Retirement%'
    OR inquiryDescription LIKE '%Retirement%'
  )

ORDER BY callDate DESC;
