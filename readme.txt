Please explain the following Review Required items in very easy English so I can understand the actual problem before discussing with business.

For each item:

1. Explain what the feature is trying to measure
2. Explain why review/business confirmation is required
3. Give one simple real-life member example
4. Explain what could go wrong if we use it without confirmation
5. Give me one simple business question I can ask in the meeting

Keep the explanation short and non-technical.

Review these items:

1. Helpline repeat contact

repeat_contact_flag

Current assumption: More than one helpline contact in the previous 90 days is treated as repeat contact.

Explain why this threshold needs business confirmation.

2. Workflow member-action filtering

Current logic counts only workflow records where member action = Internet.

Other workflow/source types seen include: Transaction Reports, Written Request, Imaging, SS Rollover, SS Contribution, ATO Comm Amendment, Mercer Easy, MST Webstpac, Telephone, SS MAAS, SALESFORCE, SUPERFACTS, ATO Portal, Newcastle Super, Kogan Super, Mercer Business Super, RF-Processor, Internal Transfer, DigitalCardBatchLoad, MST Retirement, E-mail, MercerWindow, MST GSSP, INDEX - Index Income, MST SmartSuper, Mercer MyChoice, INS_CHG - Change Ins, Transition Fail, Internet, MercerTransaction, etc.

Explain with examples why we should not simply include all of them and how business can decide which represent genuine member behaviour versus operational/system activity.

3. Full / external rollover features

rollover_withdrawal_behaviour_12m_group

These features are marked for leakage review because a full/external rollover may happen very close to actual churn.

Explain this with a very simple timeline example using:

AsOfDate -> rollover activity -> exit/churn

Show one example where the feature is safe and one where it becomes leakage.

4. Investment value-based features

investment_behaviour_12m_group

The value column meaning is not fully confirmed.

It may represent:

- market value
- allocation amount
- another investment exposure measure

Explain with simple examples how the same number could mean different things and why we should confirm the business meaning before creating features from it.

5. Campaign event features

campaign_event_behaviour_12m_group

Campaign event semantics are not fully defined in the DDL and eventName needs business confirmation.

Explain with simple examples why events such as:

- email sent
- email opened
- member clicked
- retention campaign
- account exit event

should not all be treated the same way for churn prediction.

Explain which types could be useful behaviour and which types could cause target leakage.

Output format

Please give the answer in this format for each item:

Feature / Area:
Simple meaning:
Why review is needed:
Easy example:
Risk if used incorrectly:
Business question to ask:

Do not modify any files.
Do not generate SQL.
This is explanation only.
