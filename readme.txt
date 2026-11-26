Based on David's review comments and our current ML implementation, you can provide the following responses directly in Confluence. I suggest keeping them short, business-friendly and avoiding unnecessary technical details.

### 1\. Churn definition

David's comment:

* And that the exit type is Rollover to external fund or SMSF?

* Can we agree on a formal definition of churn?

Response:

Proposed definition: Churn occurs when an account is fully exited due to a rollover to an external superannuation fund or SMSF. Internal transfers, death-related exits and other non-churn account closures are excluded.

Could you please confirm this definition, including the treatment of Inactive Low Balance Account and Trustee Voluntary Payment exits identified during historical validation?

Note: Keep this open until David confirms the formal definition. We should not finalise the target label logic before this confirmation.

### 2\. FR-ML-007 – Account eligibility

David's comment: Just confirming the distinction between datejoinedfund, which is when someone started in a specific product/subfund, compared to Tenure_Event, which captures the date someone joined the MST.

Response:

Yes, agreed. As the current ML modelling is at account level, fundJoinDate is used to determine account eligibility and account-level tenure. Tenure_Event represents overall MST membership tenure, which is a separate concept and can be considered as an additional feature if required.

### 3\. FR-ML-008 – AccountSummary requirement

David's comment: This just saying, having clean data?

Response:

Yes, essentially. This ensures that each account included in modelling has a valid AccountSummary record and sufficient information to establish its eligibility at the prediction cut-off date.

### 4\. FR-ML-009 – Feature window

David's comment: Could be worth aligning taxonomy e.g. Lookback window → cut-off date → prediction window or whatever, but be consistent?

Response:

Agreed. We will standardise the terminology across the ML documentation as Lookback Window, Prediction Cut-off Date (AsOfDate) and Prediction Window to ensure consistency.

For your understanding:

Illustration using the current proposed three-month prediction window.

### 5\. FR-ML-013 – Outcome window

David's comment: Wasn't exploration and testing meant to be applied to determine which would give the best outcomes?

Response:

Yes, agreed. The three-month prediction window is an initial baseline. We will evaluate alternative prediction windows during model experimentation and recommend the most suitable duration based on model performance, business usefulness and retention intervention lead time.

### 6\. FR-ML-025 – Risk bands

David's comment: Please confirm we will see the individual score from 0 to 1 for each account in addition to the band labels.

Response:

Yes, confirmed. The ML output will provide both the individual churn probability score between 0 and 1 and the corresponding risk band (High, Medium or Low) for each account.

### 7\. FR-ML-017 – Website engagement

David's comment: This is only a restriction for testing while in UAT and until data quality is confirmed to be good.

Response:

Yes, agreed. Website engagement remains in scope. The current limitation is due to source data unavailability in the development/testing environment. The features will remain NULL until the source is populated and data quality is validated.

### 8\. FR-ML-026 – Primary churn driver

David's comment: Needs to be the specific field that is the driver. But this will be more than one driver, right?

Response:

Yes, confirmed. The ML output will identify the specific feature contributing most significantly to the account's churn risk as the primary driver. Additional significant contributing features will be provided under additional churn drivers (FR-ML-027), where applicable.

### Impact on our current development

| Review comment               | Impact                                                             |
| ---------------------------- | ------------------------------------------------------------------ |
| Formal churn definition      | Target label changes after confirmation                            |
| Account vs MST tenure        | Existing account-level logic retained; additional feature optional |
| AccountSummary eligibility   | No immediate change                                                |
| Terminology alignment        | Documentation update                                               |
| Prediction window            | Next sprint experimentation                                        |
| Individual probability score | Already planned                                                    |
| Website engagement           | Existing NULL handling retained                                    |
| Multiple churn drivers       | Next sprint explainability implementation                          |

We can continue with Step 2 – Historical consolidated feature dataset generation. None of these comments requires an immediate redesign of our existing feature pipeline, based on the current interpretation.

The main pending business confirmation is the formal churn definition.
