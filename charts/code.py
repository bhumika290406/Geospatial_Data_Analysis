import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler


# ==========================================
# STEP 1: LOAD DATASET
# ==========================================

df = pd.read_csv("india_regional_market_v2.csv")

print("Dataset loaded successfully.")
print("Original rows:", len(df))


# ==========================================
# STEP 2: REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))


# ==========================================
# STEP 3: CREATE CITY-LEVEL DATASET
# ==========================================

city_data = df.groupby(["City", "State"]).agg({
    "MonthlySearchDemand": "sum",
    "ExistingCompetitors": "sum",
    "MedianAnnualIncomeINR": "mean",
    "LeadConversionRate": "mean",
    "EstimatedAcquisitionCostINR": "mean",
    "Latitude": "mean",
    "Longitude": "mean"
}).reset_index()


# ==========================================
# STEP 4: DEMAND VS COMPETITION RATIO
# ==========================================

city_data["DemandCompetitionRatio"] = (
    city_data["MonthlySearchDemand"] /
    (city_data["ExistingCompetitors"] + 1)
)


# ==========================================
# STEP 5: CREATE NORMALIZED SCORES
# ==========================================

scaler = MinMaxScaler()

# Demand score
city_data["DemandScore"] = scaler.fit_transform(
    city_data[["MonthlySearchDemand"]]
)

# Competition score
city_data["CompetitionScore"] = scaler.fit_transform(
    city_data[["ExistingCompetitors"]]
)

# Conversion score
city_data["ConversionScore"] = scaler.fit_transform(
    city_data[["LeadConversionRate"]]
)

# Income score
city_data["IncomeScore"] = scaler.fit_transform(
    city_data[["MedianAnnualIncomeINR"]]
)

# Lower acquisition cost = better opportunity
city_data["AcquisitionScore"] = (
    1 - scaler.fit_transform(
        city_data[["EstimatedAcquisitionCostINR"]]
    )
)


# ==========================================
# STEP 6: CALCULATE OPPORTUNITY SCORE
# ==========================================

city_data["OpportunityScore"] = (
    0.35 * city_data["DemandScore"] +
    0.25 * (1 - city_data["CompetitionScore"]) +
    0.20 * city_data["ConversionScore"] +
    0.10 * city_data["IncomeScore"] +
    0.10 * city_data["AcquisitionScore"]
)


# ==========================================
# STEP 7: CREATE CHARTS FOLDER
# ==========================================

os.makedirs("charts", exist_ok=True)


# ==========================================
# CHART 1: TOP 10 CITIES BY DEMAND
# ==========================================

top_demand = city_data.sort_values(
    "MonthlySearchDemand",
    ascending=False
).head(10)

plt.figure(figsize=(12, 6))

plt.bar(
    top_demand["City"],
    top_demand["MonthlySearchDemand"]
)

plt.title("Top 10 Cities by Monthly Search Demand")
plt.xlabel("City")
plt.ylabel("Monthly Search Demand")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/top_10_cities_demand.png",
    dpi=300
)

plt.close()


# ==========================================
# CHART 2: DEMAND VS COMPETITION
# ==========================================

plt.figure(figsize=(10, 6))

plt.scatter(
    city_data["ExistingCompetitors"],
    city_data["MonthlySearchDemand"]
)

plt.title("Demand vs Existing Competition")
plt.xlabel("Existing Competitors")
plt.ylabel("Monthly Search Demand")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "charts/demand_vs_competition.png",
    dpi=300
)

plt.close()


# ==========================================
# CHART 3: TOP 10 OPPORTUNITY REGIONS
# ==========================================

top_opportunity = city_data.sort_values(
    "OpportunityScore",
    ascending=False
).head(10)

plt.figure(figsize=(12, 6))

plt.bar(
    top_opportunity["City"],
    top_opportunity["OpportunityScore"]
)

plt.title("Top 10 Regions by Opportunity Score")
plt.xlabel("City")
plt.ylabel("Opportunity Score")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/top_10_opportunity_regions.png",
    dpi=300
)

plt.close()


# ==========================================
# CHART 4: STATE-WISE DEMAND
# ==========================================

state_demand = df.groupby("State")[
    "MonthlySearchDemand"
].sum().sort_values(
    ascending=False
).head(10)

plt.figure(figsize=(12, 6))

plt.bar(
    state_demand.index,
    state_demand.values
)

plt.title("Top 10 States by Total Search Demand")
plt.xlabel("State")
plt.ylabel("Total Search Demand")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/state_wise_demand.png",
    dpi=300
)

plt.close()


# ==========================================
# CHART 5: TOP 3 UNDERSERVED REGIONS
# ==========================================

top_3 = city_data.sort_values(
    "OpportunityScore",
    ascending=False
).head(3)

plt.figure(figsize=(10, 6))

plt.bar(
    top_3["City"],
    top_3["OpportunityScore"]
)

plt.title("Top 3 High-Potential Underserved Regions")
plt.xlabel("City")
plt.ylabel("Opportunity Score")
plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "charts/top_3_underserved_regions.png",
    dpi=300
)

plt.close()


# ==========================================
# STEP 8: SAVE ANALYSIS RESULTS
# ==========================================

city_data.to_csv(
    "city_level_analysis.csv",
    index=False
)

top_3.to_csv(
    "top_3_underserved_regions.csv",
    index=False
)


# ==========================================
# STEP 9: DISPLAY TOP 3 RESULTS
# ==========================================

print("\n==========================================")
print("TOP 3 HIGH-POTENTIAL UNDERSERVED REGIONS")
print("==========================================")

print(
    top_3[
        [
            "City",
            "State",
            "MonthlySearchDemand",
            "ExistingCompetitors",
            "LeadConversionRate",
            "OpportunityScore"
        ]
    ].to_string(index=False)
)


# ==========================================
# STEP 10: COMPLETION MESSAGE
# ==========================================

print("\n==========================================")
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("==========================================")

print("\nCharts saved inside the 'charts' folder.")
print("City-level analysis saved as: city_level_analysis.csv")
print("Top 3 regions saved as: top_3_underserved_regions.csv")