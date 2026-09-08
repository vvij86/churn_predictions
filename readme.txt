Those Overview columns are not essential if they are causing confusion, especially when the per-table worksheets already contain the correct detailed profiling.

For your Phase 2 workbook, the Overview should stay at a high-level summary. I would keep only fields that help you quickly understand the table’s ML usefulness, such as:

Table Name

Total Columns

Confirmed Candidate

Candidate with Transformation

Investigate Further

Exclude

Join Key Only

High Leakage Risk Columns

Key Candidate Feature Groups

General Comments


I would remove or avoid these from Overview unless you are 100% sure the aggregation logic is correct:

Constant Columns

100% Null Columns

High Cardinality Columns

Limited Date Coverage Columns


Those are better reviewed in the individual table worksheets because they are column-level data-quality details.

In your example, if customerDetails really has 6 columns that are 100% null but Overview says 1, then the Overview aggregation logic is wrong. Since the detailed worksheet is correct, I would not rely on that Overview metric.

You can ask Copilot to simplify the Overview and remove those unreliable summary columns rather than spending time fixing metrics you do not really need for feature selection.

A concise correction prompt would be:

> Please simplify the Phase 2 Overview worksheet. Remove these columns from Overview:

Constant Columns

100% Null Columns

High Cardinality Columns

Limited Date Coverage Columns


These are detailed column-level profiling metrics and are already available in the individual table worksheets.

Keep the Overview focused on:

Table Name

Total Columns

Confirmed Candidate

Candidate with Transformation

Investigate Further

Exclude

Join Key Only

High Leakage Risk Columns

Key Candidate Feature Groups

General Comments


Do not modify the individual table worksheets or their profiling results.



That is cleaner for your project.
