Yes. Ask only major pending questions, simple one by one. You can send this to Taj:

Hi Taj, thanks for the earlier clarification. Based on your response and the BRS, I have noted the confirmed points. To finalize the FRS for retention rate ML scope, I need confirmation only on the below major pending questions:

1. Should the retention/churn prediction be done at member level, account level, or both?

2. What is the exact retention rate formula we should use for this ML use case?

3. For account closure, should we treat it as churn/not retained only when the member has fully exited or fully rolled over out?

4. For death cases, should we exclude them from churn calculation, or treat them as not retained only if the account/FUM is fully exited?

5. For FUM retention, can we calculate it as:
   FUM at end of 12-month period / FUM at start of 12-month period?

6. For ML target label, can we define it like below?
   Retained = member/account remains with Mercer and has FUM at the end of 12 months
   Not retained/churn = full rollover out or account closure due to full exit
   Churn risk/FUM leakage = partial rollover outThis avoids asking already answered items like 12 months, full rollover, partial rollover, and dormant/inactive.
