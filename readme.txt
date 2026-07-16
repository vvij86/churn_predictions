WITH params AS (
    SELECT
        CAST('2024-12-31' AS date) AS as_of_date,
        CAST('2025-01-01' AS date) AS outcome_start_date,
        CAST('2025-03-31' AS date) AS outcome_end_date
)
SELECT
    CASE
        WHEN a.EXIT_DATE IS NULL
            THEN 'NO_EXIT_DATE'

        WHEN CAST(a.EXIT_DATE AS date) <= p.as_of_date
            THEN 'EXITED_ON_OR_BEFORE_AS_OF_DATE'

        WHEN CAST(a.EXIT_DATE AS date) >= p.outcome_start_date
         AND CAST(a.EXIT_DATE AS date) <= p.outcome_end_date
            THEN 'EXITED_IN_OUTCOME_WINDOW'

        WHEN CAST(a.EXIT_DATE AS date) > p.outcome_end_date
            THEN 'EXITED_AFTER_OUTCOME_WINDOW'

        ELSE 'REVIEW'
    END AS exit_date_category,

    a.STATUS_CODE,
    COUNT(*) AS account_count

FROM SonataODS.dbo.ACCOUNT a
CROSS JOIN params p

GROUP BY
    CASE
        WHEN a.EXIT_DATE IS NULL
            THEN 'NO_EXIT_DATE'

        WHEN CAST(a.EXIT_DATE AS date) <= p.as_of_date
            THEN 'EXITED_ON_OR_BEFORE_AS_OF_DATE'

        WHEN CAST(a.EXIT_DATE AS date) >= p.outcome_start_date
         AND CAST(a.EXIT_DATE AS date) <= p.outcome_end_date
            THEN 'EXITED_IN_OUTCOME_WINDOW'

        WHEN CAST(a.EXIT_DATE AS date) > p.outcome_end_date
            THEN 'EXITED_AFTER_OUTCOME_WINDOW'

        ELSE 'REVIEW'
    END,
    a.STATUS_CODE

ORDER BY account_count DESC;
