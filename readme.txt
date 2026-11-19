Update the existing file:

"ml_mscs_mrt_base_population.py"

Add the account fund join date to the base population output.

Requirements:

1. Do NOT change any existing business logic, filtering logic, point-in-time logic, eligibility logic, logging, exception handling, validation logic, or modelling grain.

2. Source column already available in:

"mer_wealth_dev.mer_wealth_landing_edge.mscs_mrt_account_summary"

Source field:

"fundJoinDate"

3. Include this field in the final "base_population_df".

4. Rename/alias it to:

"fund_join_date"

5. Cast it to a date type if required.

6. Final base population columns should now include, where already present:

- "account_id"
- "member_id"
- "customer_id"
- "fund_id"
- "fund_join_date"
- "as_of_date"

7. Preserve the final grain:

"one row per account_id per as_of_date"

8. Do not use "fund_join_date" as a replacement for "as_of_date".

"fund_join_date" is an account attribute representing when the account joined the fund.

"as_of_date" remains the point-in-time modelling snapshot date.

9. Keep the existing eligibility condition:

"fundJoinDate <= as_of_date"

where currently applicable.

10. Add validation for "fund_join_date":

- log null "fund_join_date" count
- verify no "fund_join_date" is after "as_of_date"
- raise an exception if records with "fund_join_date > as_of_date" are present in the final base population

11. Keep the existing duplicate and null-key validations unchanged.

12. Do not modify "ml_mscs_mrt_contribution_features.py" as part of this change unless required only to remain compatible with the updated base population schema.

13. Ensure the existing base population row count/grain is not changed solely because this additional output column is added.

14. After the change, display the sample output including "fund_join_date".

Purpose:
"fund_join_date" is required as an account-level attribute for downstream ML/Power BI output and may later be used to derive account-tenure features.
