import pandas as pd
import folium

# ==========================================
# LOAD CITY-LEVEL DATA
# ==========================================

city_data = pd.read_csv("city_level_analysis.csv")

# ==========================================
# FIND TOP 3 REGIONS
# ==========================================

top_3 = city_data.sort_values(
    "OpportunityScore",
    ascending=False
).head(3)

top_3_cities = top_3["City"].tolist()

print("\nTOP 3 HIGH-POTENTIAL REGIONS")
print(
    top_3[
        ["City", "State", "OpportunityScore"]
    ].to_string(index=False)
)


# ==========================================
# CREATE MAP WITHOUT EXTERNAL TILES
# ==========================================

market_map = folium.Map(
    location=[22.5, 78.9],
    zoom_start=5,
    tiles=None
)


# ==========================================
# ADD SIMPLE INDIA MAP OUTLINE
# ==========================================

folium.GeoJson(
    "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson",
    name="India States",
    style_function=lambda feature: {
        "fillColor": "#eeeeee",
        "color": "#555555",
        "weight": 1,
        "fillOpacity": 0.4
    }
).add_to(market_map)


# ==========================================
# ADD CITY MARKERS
# ==========================================

for _, row in city_data.iterrows():

    if row["City"] in top_3_cities:
        radius = 12
        marker_color = "red"
        label = "TOP HIGH-POTENTIAL REGION"
    else:
        radius = 6
        marker_color = "blue"
        label = "Other Market"

    popup_text = f"""
    <div style="font-size:14px">

    <b>City:</b> {row['City']}<br>
    <b>State:</b> {row['State']}<br><br>

    <b>Monthly Search Demand:</b>
    {row['MonthlySearchDemand']:.0f}<br>

    <b>Existing Competitors:</b>
    {row['ExistingCompetitors']:.0f}<br>

    <b>Lead Conversion Rate:</b>
    {row['LeadConversionRate']:.2%}<br>

    <b>Median Annual Income:</b>
    ₹{row['MedianAnnualIncomeINR']:.0f}<br>

    <b>Acquisition Cost:</b>
    ₹{row['EstimatedAcquisitionCostINR']:.0f}<br>

    <b>Opportunity Score:</b>
    {row['OpportunityScore']:.4f}

    </div>
    """

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=radius,
        popup=folium.Popup(
            popup_text,
            max_width=350
        ),
        tooltip=f"{row['City']} - {label}",
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.8
    ).add_to(market_map)


# ==========================================
# ADD LEGEND
# ==========================================

legend_html = """
<div style="
position: fixed;
bottom: 30px;
left: 30px;
z-index: 9999;
background-color: white;
padding: 15px;
border: 2px solid grey;
border-radius: 8px;
font-size: 14px;
">

<b>Market Opportunity</b><br><br>

<span style="
display:inline-block;
width:14px;
height:14px;
background:red;
border-radius:50%;
"></span>

&nbsp; Top 3 High-Potential Regions

<br><br>

<span style="
display:inline-block;
width:14px;
height:14px;
background:blue;
border-radius:50%;
"></span>

&nbsp; Other Cities

</div>
"""

market_map.get_root().html.add_child(
    folium.Element(legend_html)
)


# ==========================================
# ADD TITLE
# ==========================================

title_html = """
<div style="
position: fixed;
top: 10px;
left: 50%;
transform: translateX(-50%);
z-index: 9999;
background-color: white;
padding: 10px 20px;
border-radius: 8px;
box-shadow: 0 2px 6px rgba(0,0,0,0.3);
font-size: 20px;
font-weight: bold;
">
Geospatial Market Opportunity Analysis
</div>
"""

market_map.get_root().html.add_child(
    folium.Element(title_html)
)


# ==========================================
# SAVE MAP
# ==========================================

market_map.save(
    "regional_market_map.html"
)

print("\nInteractive map created successfully!")
print("Saved as: regional_market_map.html")