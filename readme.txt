USE CATALOG mer_wealth_dev;
USE SCHEMA mer_wealth_mra_mlops;

CREATE OR REPLACE TABLE _ml_write_test
AS
SELECT
    1 AS test_id,
    current_timestamp() AS created_at;

SELECT * FROM _ml_write_test;

DROP TABLE _ml_write_test;
