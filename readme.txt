Please inspect the current:

build_merceredge_base_historical_dataset.sql

and explain exactly how the four modelling dates are currently managed:

- @FeatureStartDate
- @AsOfDate
- @OutcomeStartDate
- @OutcomeEndDate

Do not modify the SQL.

For each date parameter, explain:

1. Is it manually supplied or derived?
2. What is its purpose?
3. Which source tables use it?
4. Which exact source date column is compared against it?
5. Whether the comparison is for:
   - account eligibility
   - historical feature/event window
   - partial point-in-time state
   - target/outcome logic

Create a table like:

Source Table | Source Date Column | FeatureStartDate Used? | AsOfDate Used? | Outcome Window Used? | Purpose

Please cover all 18 in-scope MercerEdge tables, but clearly mark tables that are not currently used by the base dataset SQL.

Important:
- Do not guess column names.
- Read the current SQL and DDL files.
- Do not change any code.
- Clearly distinguish:
  * manually supplied modelling dates
  * source event dates
  * target/outcome dates
  * join/commencement/effective dates

Also explain the first training snapshot:

FeatureStartDate = 2023-04-01
AsOfDate = 2024-03-31
OutcomeStartDate = 2024-04-01
OutcomeEndDate = 2024-06-30

and show exactly which source columns are filtered against those dates.
