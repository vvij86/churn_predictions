Review ONLY the Workflow Behaviour section in "behavioural_features_business_review.sql".

Do not change any other feature block.

Use the existing live database connection pattern already available in "sample.py" to validate the Workflow features against the live UAT source data.

The objective is to review the Workflow features against the client comments, identify overlap/duplication, validate coverage, and recommend whether each feature should be KEPT, REVIEWED, RENAMED, or DE-SCOPED.

Important rules:

- Do not change the SQL initially.
- First perform live validation and show evidence.
- Keep the modelling grain at one row per accountID per AsOfDate.
- Use only source data on or before "@AsOfDate".
- Respect the existing 12-month feature window.
- Do not use future/post-AsOfDate information.
- Do not assume that a feature is useful just because records exist.
- Do not infer business meaning only from the feature name.
- Base conclusions on the actual source columns, job codes, job descriptions, workflow status, event dates, and live data.
- Check whether Workflow features duplicate signals already captured in Helpline, Campaign/Event, Contribution, Rollover, Investment or other existing behavioural blocks.
- Do not modify unrelated features.

1. Review every Workflow feature currently present

For each active Workflow feature, return:

- feature name
- exact source table
- exact source column(s)
- source values / JobCodes / JobDescriptions used
- business meaning
- record count in 12-month window
- distinct account count in 12-month window
- recent 90-day coverage where applicable
- recent 30-day coverage where applicable
- representative raw examples
- overlap with other existing feature blocks
- recommendation:
  - KEEP
  - KEEP – DISTINCT SIGNAL
  - REVIEW
  - RENAME
  - DE-SCOPE

Also identify any feature names that are unclear and recommend a more self-explanatory name where needed.

2. Validate account-level grain

Confirm that the final Workflow aggregation produces:

- one row per "accountID"
- duplicate accountID count = 0

Raw Workflow data may naturally contain repeated accountIDs because one account can have multiple workflow records. That is acceptable.

Only the final aggregated Workflow feature result must have one row per accountID.

Return:

- raw/event-level repeated accountIDs = X
- final aggregated duplicate accountIDs = X
- final Workflow grain = one row per accountID: YES / NO

3. Validate date integrity

Check that Workflow records entering the feature logic satisfy:

"workflow_date >= @FeatureStartDate"
and
"workflow_date <= @AsOfDate"

Return:

- post-AsOfDate rows entering feature logic = X
- pre-FeatureStartDate rows entering feature logic = X
- PASS / FAIL

Do not report total source-table rows after AsOfDate unless they actually enter the feature logic.

4. Special review – Complaint Escalation

The client comment for the Workflow complaint-escalation feature says "As above".

Interpret this as referring to the earlier Helpline complaint concern:

Helpline complaints may represent only a small subset of all complaints and broader complaint information may exist in another source/workbook.

Therefore perform a specific validation of the Workflow complaint-escalation feature.

Do NOT automatically keep or de-scope it.

Check:

1. What exact Workflow "JobCode", "JobDescription", status, type, or other source values define complaint escalation?
2. Number of Workflow complaint-escalation records in the 12-month window.
3. Distinct accounts with complaint escalation.
4. 90-day coverage.
5. 30-day coverage if available.
6. Show representative raw source records.
7. Compare against the Helpline complaint feature.
8. Calculate account overlap between:
   - Workflow complaint escalation
   - Helpline complaint activity
9. Determine whether Workflow complaint escalation represents:
   - the same generic complaint behaviour,
   - a subset of Helpline complaints,
   - an escalation/severity signal,
   - or a distinct operational workflow.
10. Check whether Workflow complaint escalation itself appears to represent only a subset of overall complaint activity.

Return specifically:

- Workflow complaint escalation accounts = X
- Helpline complaint accounts = X
- Accounts in both = X
- % of Workflow complaint accounts also appearing in Helpline = X%
- Exact Workflow complaint rule = ...
- Example Workflow descriptions = ...
- Interpretation = ...
- Recommendation = KEEP / KEEP – DISTINCT ESCALATION SIGNAL / REVIEW / DE-SCOPE

Important:

Do not de-scope Workflow complaint escalation merely because Helpline complaint features were de-scoped.

If Workflow complaint escalation represents a stronger event such as a complaint being formally escalated, transferred to a specialist team, or moved into an escalation workflow, treat it as potentially more meaningful than a generic complaint count.

However, do not treat it as complete complaint coverage unless the data supports that conclusion.

5. Check duplication with Helpline

For each relevant Workflow feature, check account-level overlap with related Helpline features.

Especially review potential overlaps involving:

- complaint
- advice
- retirement / pension
- rollover / consolidation
- contribution
- member service

For each overlap return:

- Workflow accounts = X
- matching Helpline accounts = X
- accounts in both = X
- overlap % = X
- same business meaning? YES / NO / PARTIAL
- recommendation

Do not remove a feature simply because some overlap exists.

If the Workflow event represents a materially different stage, severity or action, state that clearly.

Example:

Helpline complaint inquiry = member contacted Helpline about a complaint.

Workflow complaint escalation = complaint progressed into an operational escalation workflow.

These may be related but not necessarily duplicate signals.

6. Review generic versus specific Workflow activity

Identify whether any Workflow feature is merely measuring broad operational activity such as:

- number of jobs
- number of workflow records
- generic completed jobs
- generic active jobs

If a feature only measures generic workflow volume without clear business meaning, mark it as:

"REVIEW – generic activity / likely low signal"

Do not automatically remove it. Show live coverage and business interpretation first.

Prefer specific business-action signals over generic activity counts.

7. Review Workflow completion/status logic

Where Workflow features depend on statuses such as:

- completed
- open
- cancelled
- pending
- failed
- closed

validate whether the feature should use:

- all records,
- completed records only,
- or another specific subset.

Show the actual source status distribution before recommending any change.

Do not invent status logic.

8. Check potential target leakage

Review Workflow event names / JobCodes / descriptions for any event that directly represents or occurs only because of:

- full member exit
- account closure
- full rollover out
- completed external transfer caused by exit
- cancellation after member exit
- other clearly post-churn operational events

Flag such events as potential target leakage.

Do not use post-exit Workflow events as predictive behavioural features.

Return:

- potential leakage event value
- why it may leak the target
- recommendation

Do not modify the SQL until the leakage assessment is complete.

9. Final output

Return a concise table with:

| Feature | Coverage | Business Meaning | Overlap | Client Comment Addressed | Recommendation |

Also provide:

PASS / REVIEW / FAIL summary

- Date integrity: PASS / FAIL
- Account-level grain: PASS / FAIL
- Complaint escalation review: PASS / REVIEW / FAIL
- Duplication review: PASS / REVIEW / FAIL
- Target leakage review: PASS / REVIEW / FAIL
- Feature naming clarity: PASS / REVIEW

Then provide a short section:

Recommended SQL changes

List only the SQL changes you recommend.

Do NOT make the changes yet.

For every recommended change explain in one short sentence why it is required.

Do not touch Website Engagement. Website Engagement is out of scope for this review and will be handled separately.
