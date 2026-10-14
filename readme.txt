Review the executed Step 3 validation results in:

build_merceredge_feature_dataset_step3.sql

Do NOT start Step 4 yet.

The current validation shows:

- row_count_before_step3 = 837435
- row_count_after_step3 = 837435
- duplicate_account_id_asof_count = 0
- step2_churn_rows = 15291
- step3_churn_rows = 15291
- step2_retained_rows = 822144
- step3_retained_rows = 822144
- POINT_IN_TIME_SAFETY = FAIL

Please investigate and fix only the point-in-time validation issue.

Requirements:

1. Identify exactly why POINT_IN_TIME_SAFETY is FAIL.

2. For every Step 3 campaign/event feature, prove that only source events satisfying:

   eventDate >= @FeatureStartDate
   AND eventDate <= @AsOfDate

   are used in feature calculations.

3. Add explicit validation counts for:
   - source events before @FeatureStartDate
   - source events after @AsOfDate
   - source events within the valid feature window
   - future events accidentally used in engineered features

4. The count of future events actually contributing to predictive features must be 0.

5. MEMBER_EXIT must not be used as a predictive feature.
   It may be profiled for validation only.

6. Also review other potentially leakage-prone event types such as:
   - PAYMENT_EXTERNAL
   - ROLLOVER
   - ROLLIN
   - PENSION
   - ALLOCATED_PENSION
   - any event representing exit, closure, final payment, or outcome processing

7. Do not automatically remove these event types unless required.
   Classify unclear event types as REVIEW REQUIRED.

8. Do not change:
   - target_churn
   - retained_flag
   - eligibility logic
   - Step 1 features
   - Step 2 features
   - row grain

9. After correction, rerun validation and report:

   POINT_IN_TIME_SAFETY = PASS or FAIL

   future_events_used_in_features = 0

   row_count_before_step3
   row_count_after_step3
   duplicate_count
   churn count before/after
   retained count before/after

10. If POINT_IN_TIME_SAFETY still fails, clearly state the exact feature(s), event type(s), and reason.

Stop after Step 3 is corrected and validated.
