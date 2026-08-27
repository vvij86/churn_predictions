Copilot Prompt — Add Scoring Date to Batch Scoring CSV Filename

Update the existing notebook:

"07_batch_scoring_using_champion_alias"

Modify only the CSV output filename logic.

Currently the notebook saves the output as:

"Output_Metrics/champion_batch_scoring_output.csv"

Change it so the filename includes the scoring date in "YYYYMMDD" format.

For example:

"Output_Metrics/champion_batch_scoring_output_20260827.csv"

Use the current UTC scoring date.

Example approach:

from datetime import datetime, timezone

scoring_date = datetime.now(timezone.utc).strftime("%Y%m%d")

output_path = f"Output_Metrics/champion_batch_scoring_output_{scoring_date}.csv"

Then save:

scoring_output.to_csv(output_path, index=False)

Print the generated output path after saving.

Also ensure the "scoring_timestamp" column inside the dataframe remains unchanged.

Do not modify:

- model loading logic
- Champion alias logic
- predictions
- risk-band logic
- model metadata
- any other Step 7 functionality

Add a short Markdown note explaining that date-stamped filenames preserve the scoring output from each scheduled run instead of overwriting the previous file.
