%sql

SELECT DISTINCT
    as_of_date,
    DATE_ADD(as_of_date, 1) AS outcome_start_date,
    LAST_DAY(ADD_MONTHS(as_of_date, 6)) AS outcome_end_date,
    CASE
        WHEN LAST_DAY(ADD_MONTHS(as_of_date, 6))
             <= DATE '2026-10-16'
        THEN 'ELIGIBLE'
        ELSE 'INCOMPLETE_OUTCOME'
    END AS outcome_status
FROM mer_wealth_dev.mer_wealth_mra_mlops.member_retention_features
ORDER BY as_of_date;
