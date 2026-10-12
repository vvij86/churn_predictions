You can ask business these in very simple English:

- What should be the AsOfDate / prediction date for each training snapshot — month end, quarter end, or another date?
- How much past history should we use before each AsOfDate — 12 months, shorter for new members, or something else?
- How far into the future should we check for churn after each AsOfDate — 3 months or another period?
- Should OutcomeStartDate always be the next day after AsOfDate?
- For accounts that joined recently, can we include them with less than 12 months of history?
- What is the minimum history/tenure required before an account can be included in training?
- Should accounts that exited on the AsOfDate be excluded from the active population?
- Should accounts that exit after the AsOfDate but within the outcome window be treated as churn?
- For model validation, do you agree with using time-based validation instead of randomly splitting accounts?
- Which periods should be used for training, validation, and final test/holdout?
- Should the final holdout period be kept completely untouched until the model is finalized?
- How often should we create historical training snapshots — monthly or quarterly?
- Business asked to use data from 1-Apr-2023. Should that mean the earliest source-history date, with the first full 12-month snapshot at 31-Mar-2024?
- Are there any business periods we should exclude because of unusual events, migrations, or data-quality issues?
- For production scoring, how often should the model score members — weekly, monthly, or quarterly?
- How often should the model be retrained?

For your meeting, the most important ones are probably the first 10.
