import pandas as pd

df = pd.read_csv("india_regional_market_v2.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())
print(df.duplicated().sum())
df = df.drop_duplicates()
city_data = df.groupby(["City", "State"]).agg({
    "MonthlySearchDemand": "sum",
    "ExistingCompetitors": "sum",
    "MedianAnnualIncomeINR": "mean",
    "LeadConversionRate": "mean",
    "EstimatedAcquisitionCostINR": "mean",
    "Latitude": "mean",
    "Longitude": "mean"
}).reset_index()
city_data["DemandCompetitionRatio"] = (
    city_data["MonthlySearchDemand"] /
    (city_data["ExistingCompetitors"] + 1)
)
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

city_data["DemandScore"] = scaler.fit_transform(
    city_data[["MonthlySearchDemand"]]
)

city_data["CompetitionScore"] = scaler.fit_transform(
    city_data[["ExistingCompetitors"]]
)

city_data["ConversionScore"] = scaler.fit_transform(
    city_data[["LeadConversionRate"]]
)

city_data["IncomeScore"] = scaler.fit_transform(
    city_data[["MedianAnnualIncomeINR"]]
)

city_data["AcquisitionScore"] = 1 - scaler.fit_transform(
    city_data[["EstimatedAcquisitionCostINR"]]
)

city_data["OpportunityScore"] = (
    0.35 * city_data["DemandScore"] +
    0.25 * (1 - city_data["CompetitionScore"]) +
    0.20 * city_data["ConversionScore"] +
    0.10 * city_data["IncomeScore"] +
    0.10 * city_data["AcquisitionScore"]
)
top_regions = city_data.sort_values(
    "OpportunityScore",
    ascending=False
).head(3)

print(top_regions)