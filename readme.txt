Yes. Ask Copilot to inspect your full .sql DDL script and identify whether the tables/columns needed to derive each churn event exist, rather than searching only for columns literally named full_withdrawal or full_rollover.

You can paste this prompt into Copilot:

> Please analyse the complete attached/open .sql DDL script containing the MercerEDGE table definitions.

I need to determine whether the database has enough columns to identify the following business events:

1. Full withdrawal


2. Full rollover out / full transfer out


3. Account closure


4. Partial rollover out


5. Partial withdrawal


6. Death-related exit



Do not search only for exact column names such as full_withdrawal_flag. Also look for columns that could be used to derive these events, such as:

transaction/event type

transaction amount

rollover amount/type/direction

withdrawal amount/type

account balance

account status/status reason

account close/termination/exit date

exit reason/type

member status

death/deceased indicator or reason

transfer/rollover destination or source


For each of the 6 events, provide:

Available: Yes / No / Possibly

Table name

Relevant column name(s)

Data type

How the event could potentially be derived

Any missing information or ambiguity that needs business confirmation


Please produce the result as a table:

Business Event | Available? | Table | Relevant Columns | Possible Derivation Logic | Gap / Question

Important: Do not assume that a column proves the business rule. Clearly distinguish between:

an explicit event/flag available directly in the data, and

an event that would need to be derived from multiple columns.


Also list any additional tables or columns in the DDL that appear relevant to customer/member churn or retention.



This is better than asking “Are full withdrawal columns there?”, because in your data it may be represented indirectly—for example, an exit_type_code, transaction event, account status, and amount combination rather than one obvious full_withdrawal column.

For your current Excel clarification sheet, this Copilot output should help you answer rows like full rollover, full withdrawal, account closure, partial events and death exits before you go back to the SME for the actual business-rule confirmation.
