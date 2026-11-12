Review ONLY the "Insurance Behaviour / Cover Position" feature block in behavioural_features_business_review.sql.

Do NOT modify any other feature section.
Do NOT change the consolidated dataset SQL.
Do NOT change Website Engagement or any previously reviewed section yet.

The current Insurance features in the business-review document are:

1. has_death_cover_asof
2. death_cover_amount_asof
3. has_tpd_cover_asof
4. tpd_cover_amount_asof
5. has_ip_cover_asof
6. ip_cover_amount_asof
7. insurance_cover_type_count_asof

Source:
edgeSource.accountInsuranceCurrent

Client/business review concerns:
- Death cover amount: "Not confident that the Death Cover Amount tells us anything important."
- TPD cover amount: "Not confident that the TPD Cover Amount tells us anything important."
- IP cover amount: "Not confident that the IP Cover Amount tells us anything important. FYI IP is Income Protection (Salary Continuation Insurance) if that helps."

Goal:
Determine which insurance features are defensible churn/retention behavioural or position features and which are weak, redundant, low-value, or should be de-scoped.

IMPORTANT:
Do not assume that a larger insurance amount means stronger engagement.
Do not infer business meaning from the feature name alone.
Base every conclusion on:
- actual SQL logic
- actual source columns and values
- live account-level coverage
- distribution
- relationship between cover flags and amounts
- account-level uniqueness
- as-of-date safety
- overlap/redundancy between features

STEP 1 — Inspect the existing Insurance SQL

Identify exactly:
- how the latest/as-of insurance record is selected
- which source date column is used
- whether records after @AsOfDate are excluded
- whether the feature grain is one row per accountID
- how Death, TPD and IP cover are identified
- how the amount fields are aggregated
- how insurance_cover_type_count_asof is calculated

Do not change SQL yet.

STEP 2 — Run live-source validation

Using the same SQL Server connection pattern already used successfully in sample.py, validate the Insurance section against live data.

For each feature calculate:

A. has_death_cover_asof
- accounts = 1
- accounts = 0
- NULL count
- percentage of eligible accounts with Death cover

B. death_cover_amount_asof
For accounts with Death cover:
- non-null account count
- zero count
- min
- median
- average
- p25
- p75
- p90
- p95
- max
- number of distinct values

Check whether amount is strongly concentrated around standard/default values or varies meaningfully.

C. has_tpd_cover_asof
Same coverage checks as Death.

D. tpd_cover_amount_asof
Same distribution checks as Death.

E. has_ip_cover_asof
Same coverage checks.

F. ip_cover_amount_asof
Same distribution checks.

Remember:
IP = Income Protection / Salary Continuation Insurance.

G. insurance_cover_type_count_asof
Report distribution for:
- 0
- 1
- 2
- 3
and any unexpected values.

STEP 3 — Check amount vs flag redundancy

For each insurance type answer:

- Can amount > 0 be used to infer the same thing as the flag?
- Are there accounts where flag = 1 but amount is NULL or 0?
- Are there accounts where flag = 0 but amount > 0?
- Is the amount therefore adding information beyond simple cover presence?

Report counts for each mismatch.

STEP 4 — Check redundancy across Death / TPD / IP

Calculate account overlap:

- Death only
- TPD only
- IP only
- Death + TPD
- Death + IP
- TPD + IP
- Death + TPD + IP
- no cover

Compare this with insurance_cover_type_count_asof.

Validate:

insurance_cover_type_count_asof
=
number of active insurance cover types

If not, explain why.

STEP 5 — Assess whether raw cover amounts are meaningful

For death_cover_amount_asof, tpd_cover_amount_asof and ip_cover_amount_asof, specifically test Nathan's concern.

Do NOT call an amount useful simply because it varies.

Assess whether the amount represents:
- member behaviour
- current insurance position
- product/default configuration
- salary/FUM/member circumstances
- or something else

If practical from the available source data, test whether large amounts mainly correspond to:
- particular products
- salary-related insurance
- account/member characteristics
rather than an intentional engagement action.

Classify each amount feature as:

KEEP
REVIEW
DE-SCOPE

with a short evidence-based reason.

STEP 6 — Assess the flags separately

Assess:

- has_death_cover_asof
- has_tpd_cover_asof
- has_ip_cover_asof

Ask whether presence/absence of cover is more defensible than absolute monetary amount.

Do NOT automatically de-scope the flags just because the amounts may be weak.

STEP 7 — Assess insurance_cover_type_count_asof

Determine whether this adds information beyond the three individual flags.

Check:

insurance_cover_type_count_asof
versus
has_death_cover_asof + has_tpd_cover_asof + has_ip_cover_asof

If mathematically equivalent, state that it is a derived summary and assess whether:
- keeping the individual flags is sufficient, OR
- count is useful as a compact feature, OR
- retaining both would be redundant.

STEP 8 — Technical integrity checks

Confirm:

- post-@AsOfDate rows entering feature logic = 0
- duplicate final accountID count = 0
- final grain = one row per accountID
- no future insurance state is used
- NULL handling is sensible
- no obvious leakage

STEP 9 — Final decision table

Return:

Feature | Live coverage | Business meaning | Redundancy concern | Recommendation | Reason

for all 7 features.

Use only:
KEEP
REVIEW
DE-SCOPE

STEP 10 — Final recommendation

Return three concise lists:

KEEP:
...

REVIEW:
...

DE-SCOPE:
...

Then provide a short business-review comment for each feature that I can paste into the client review document.

Examples of the style I need:

"Retained — cover presence provides a current insurance-position indicator; validated against live source data."

or

"De-scoped — absolute cover amount is primarily a financial/product-position measure and did not show sufficient independent behavioural value."

Do not edit the SQL in this step.

First provide the evidence-based review and recommendation only.

If a feature should be removed or renamed, clearly state it, but wait for my next instruction before making any SQL change.
