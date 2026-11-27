%sql

SELECT
    MIN(exitDate) AS earliest_exit_date,
    MAX(exitDate) AS latest_exit_date,
    COUNT(*) AS total_records,
    COUNT(exitDate) AS exit_records
FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary;


%sql

SELECT
    MIN(processedDate) AS earliest_payment_date,
    MAX(processedDate) AS latest_payment_date,
    COUNT(*) AS total_records,
    COUNT(processedDate) AS payment_records
FROM mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_rollover_payment;
