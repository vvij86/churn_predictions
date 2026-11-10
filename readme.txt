Review only the Inflow Signals / Contribution Change section in "behavioural_features_business_review.sql".

Do not modify any other feature section yet.

Source table:
"edgeSource.accountMoneyInflow"

Context:
We already reviewed the main Contribution Behaviour block. Many raw/current contribution amount features may overlap with features already present there.

Nathan’s business review comments also indicate that some current amount features may be duplicates. However, the colour coding suggests that the change % and cessation flag features should not automatically be removed and may be useful behavioural signals.

Please validate the following feature families separately:

Employer SG:

- "employer_sg_current_amount_12m"
- "employer_sg_change_pct_12m"
- "employer_sg_cessation_flag"

Salary Sacrifice:

- "salary_sacrifice_current_amount_12m"
- "salary_sacrifice_change_pct_12m"
- "salary_sacrifice_cessation_flag"

Member Voluntary:

- "member_voluntary_current_amount_12m"
- "member_voluntary_change_pct_12m"
- "member_voluntary_cessation_flag"

Perform the following review using the live source data.

1. Check duplication against the already retained Contribution Behaviour features.

For each "*_current_amount_12m" feature, identify the closest existing Contribution Behaviour feature, such as:

- "employer_sg_amount_12m"
- "salary_sacrifice_amount_12m"
- "member_voluntary_amount_12m"

Determine whether the current amount feature is:

- exactly the same measure,
- derived from the same source rows,
- materially equivalent,
- or genuinely different.

If it is effectively the same information, recommend DE-SCOPE as duplicate.

Do not remove it merely because it comes from the same source table. Confirm the actual calculation first.

2. Review the "*_change_pct_12m" features separately.

Do not classify these as duplicates simply because their underlying amounts already exist.

Validate whether each feature measures a meaningful within-account behavioural change, for example:

current-period contribution amount versus prior-period contribution amount.

Check:

- source coverage,
- number of distinct accounts,
- NULL / zero handling,
- denominator logic,
- extreme percentage values,
- divide-by-zero handling,
- whether the comparison periods are truly comparable,
- whether the feature uses only data available on or before "@AsOfDate".

If technically valid, treat these as potentially useful behavioural change signals and recommend KEEP unless evidence shows otherwise.

3. Review the "*_cessation_flag" features separately.

Validate exactly how cessation is defined.

Confirm that a cessation flag means something equivalent to:

prior contribution activity existed,
but contribution activity stopped in the relevant recent/current period.

Check that it is not simply triggered by:

- missing data,
- incomplete source coverage,
- account closure,
- death,
- internal transfer,
- source-system gaps,
- or another technical condition.

If the flag genuinely represents contribution stopping, treat it as a potentially useful behavioural signal and recommend KEEP.

4. Pay special attention to Nathan’s review intent.

The intended interpretation is:

- raw/current contribution amount by itself does not necessarily represent stronger engagement;
- raw/current amount fields may already be represented in the Contribution Behaviour section;
- relative change in contribution behaviour can be more informative;
- cessation can be a meaningful behavioural deterioration signal.

Therefore do NOT automatically de-scope all nine features.

Expected likely pattern, subject to live-data validation:

"*_current_amount_12m"
→ possible duplicate / DE-SCOPE if equivalent to existing amount feature.

"*_change_pct_12m"
→ potentially useful / KEEP if calculation is valid.

"*_cessation_flag"
→ potentially useful / KEEP if it represents genuine contribution cessation.

5. Validate time-window integrity.

Confirm:

- no records after "@AsOfDate" enter feature logic;
- no records before "@FeatureStartDate" enter the 12-month feature logic;
- no future information is used to determine cessation;
- final feature grain is one row per "accountID";
- final duplicate "accountID" count = 0.

6. Return a decision table with:

Feature | Existing overlapping feature | Live coverage | Same underlying measure? | Business meaning | Recommendation | Reason

Use only:

- KEEP
- DE-SCOPE
- REVIEW

7. Also return a short final active feature recommendation grouped as:

KEEP:

- useful change features
- useful cessation features

DE-SCOPE:

- confirmed duplicate amount features

REVIEW:

- anything where equivalence or business meaning cannot be proven from the source data.

Important:
Do not change the SQL in this step.

First perform the live-data validation and give me the evidence-based recommendation only.

Do not assume that the green rows are automatically correct; use them as Nathan’s review direction, then confirm using live source data.

Do not infer business meaning from feature names alone. Base the conclusion on the actual SQL calculations and source values.
