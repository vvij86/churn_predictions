Use this complete Copilot prompt:

> Review the existing MercerEdge churn-driver EDA and create a new Excel workbook named: MercerEdge_ML_Churn_Driver_EDA_Remaining_Tables.xlsx

Do not modify the existing 17-table EDA workbook.

The following 17 tables have already been explored and should be used only for overlap/duplicate comparison:

1. MERCEREDGE.EDGEPORTALSOURCE.CUSTOMERDETAILS


2. MERCEREDGE.EDGEPORTALSOURCE.ACCOUNTINSURANCE


3. MERCEREDGE.EDGEPORTALSOURCE.ACCOUNTMONEYINFLOW


4. MERCEREDGE.EDGEPORTALSOURCE.ACCOUNTROLLOVERPAYMENT


5. MERCEREDGE.EDGESOURCE.ACCOUNT


6. MERCEREDGE.EDGESOURCE.ACCOUNTENGAGEMENTHELPLINE


7. MERCEREDGE.EDGESOURCE.ACCOUNTENGAGEMENTWEB


8. MERCEREDGE.EDGESOURCE.ACCOUNTINVESTMENTS


9. MERCEREDGE.EDGESOURCE.ACCOUNTMONEYINFLOW


10. MERCEREDGE.EDGESOURCE.ACCOUNTNETMONEYFLOW


11. MERCEREDGE.EDGESOURCE.ACCOUNTROLLOVERPAYMENT


12. MERCEREDGE.EDGESOURCE.ACCOUNTSUMMARY


13. MERCEREDGE.EDGESOURCE.CRN


14. MERCEREDGE.EDGESOURCE.CUSTOMERMAPPING


15. MERCEREDGE.EDGESOURCE.CUSTOMERSUMMARY


16. MERCEREDGE.EDGESOURCE.THIRDPARTYAUTHORITY


17. MERCEREDGE.TABLEAU.FUNDLISTSOURCE



These tables were newly added by the Data Modeller and must be fully explored:

MercerEdge.Edge.accountEngagementWorkflow

MercerEdge.edgePortalSource.pensionerData

MercerEdge.EdgeSource.AccountInsuranceCurrent

MercerEdge.EdgeSource.campaignEventDetails

MercerEdge.EdgeSource.campaignEvents


I am also considering these additional tables:

MercerEdge.edgePortalSource.accountDetails

MercerEdge.edgeSource.accountInteractions

MercerEdge.edgeSource.campaign

MercerEdge.edgeSource.campaignAccountMapping


For these 4 candidate tables, first compare them against the previously explored 17 tables at column level, business meaning level, and actual data-content level.

If the same or equivalent information is already available in the existing 17 tables, mark the candidate table as Not Needed and clearly identify the existing table and columns that already cover it.

If the candidate table contains additional useful information for churn prediction, mark it as Needed and perform full data exploration.

For every mandatory table and every candidate table marked Needed, create one worksheet per table and capture:

Table name

Row count

Column name

Data type

Key role / join key

Business meaning

Date columns

Null count

Null %

Distinct count

Sample values

Duplicate/key issues

Potential churn-driver relevance

Pre-churn predictive usefulness

Target leakage risk

Recommended use: Include / Exclude / Reference only

Reason for recommendation


Also create a Summary worksheet containing one row per reviewed table with:

Table name

Mandatory or Candidate

Needed / Not Needed

Main useful information

Overlap with existing 17 tables

Existing table/columns covering the same information

Churn prediction usefulness

Target leakage risk

Final recommendation


Important modelling rules:

Target grain is one row per account per as_of_date

Focus only on information available before churn

Do not recommend post-churn or outcome fields as predictive features

Treat fields such as account closure, member exit, full rollover completion or similar outcome events carefully as possible target leakage

Lower-level event or interaction data should ultimately be aggregatable to account level

Prefer features that can support a 12-month historical feature window


Keep the Excel layout and formatting similar to the existing MercerEdge churn-driver EDA workbook, with filters, readable column widths, wrapped text and clear headers.
