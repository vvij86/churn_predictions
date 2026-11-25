from ml_mscs_mrt_base_population import run_base_population_pipeline
from ml_mscs_mrt_contribution_features import run_contribution_feature_pipeline
from ml_mscs_mrt_rollover_features import run_rollover_feature_pipeline
from ml_mscs_mrt_investment_features import run_investment_feature_pipeline
from ml_mscs_mrt_helpline_features import run_helpline_feature_pipeline
from ml_mscs_mrt_campaign_features import run_campaign_feature_pipeline
from ml_mscs_mrt_web_engagement_features import run_web_engagement_feature_pipeline
from ml_mscs_mrt_third_party_authority_features import run_third_party_authority_feature_pipeline
from ml_mscs_mrt_insurance_features import run_insurance_feature_pipeline




AS_OF_DATE = "2023-04-30"

base_df = run_base_population_pipeline(
    spark=spark,
    as_of_date=AS_OF_DATE
)

base_df.createOrReplaceTempView(
    "tmp_base_population"
)




params = {
    "spark": spark,
    "as_of_date": AS_OF_DATE,
    "base_population_df": base_df
}

contrib_df = run_contribution_feature_pipeline(**params)
rollover_df = run_rollover_feature_pipeline(**params)
invest_df = run_investment_feature_pipeline(**params)
helpline_df = run_helpline_feature_pipeline(**params)
campaign_df = run_campaign_feature_pipeline(**params)
web_df = run_web_engagement_feature_pipeline(**params)
tpa_df = run_third_party_authority_feature_pipeline(**params)
insurance_df = run_insurance_feature_pipeline(**params)






contrib_df.createOrReplaceTempView("tmp_contribution_features")
rollover_df.createOrReplaceTempView("tmp_rollover_features")
invest_df.createOrReplaceTempView("tmp_investment_features")
helpline_df.createOrReplaceTempView("tmp_helpline_features")
campaign_df.createOrReplaceTempView("tmp_campaign_features")
web_df.createOrReplaceTempView("tmp_web_engagement_features")
tpa_df.createOrReplaceTempView("tmp_third_party_authority_features")
insurance_df.createOrReplaceTempView("tmp_insurance_features")








schema = "mer_wealth_dev.mer_wealth_landing_edge"

sources = {
    "tmp_src_contribution": "mscs_mrt_account_money_inflow",
    "tmp_src_rollover": "mscs_mrt_account_rollover_payment",
    "tmp_src_investment": "mscs_mrt_account_investments",
    "tmp_src_helpline": "mscs_mrt_account_engagement_helpline",
    "tmp_src_campaign_event_details": "mscs_mrt_campaign_event_details",
    "tmp_src_web": "mscs_mrt_account_engagement_web",
    "tmp_src_third_party_authority": "mscs_mrt_third_party_authority"
}

for view_name, table_name in sources.items():
    spark.table(
        f"{schema}.{table_name}"
    ).createOrReplaceTempView(view_name)







