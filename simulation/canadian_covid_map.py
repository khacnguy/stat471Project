import pandas as pd
import geopandas as gpd
import plotly.express as px
import json

# df = pd.read_csv("ca_pr_day_n.csv")   
# df['category'] = ''
# print(df)
f = open('result.json')
data = json.load(f)
data_reformat = []
for year in data.keys():
    for location in data[year]:
        tmp = {"year": year, "category": data[year][location], "CDUID": location[-4:]}
        data_reformat.append(tmp)
df = pd.DataFrame(data_reformat)
print(df)

mp = gpd.read_file("lcd_000a21g_e.geojson")
# simplify geometry to 1000m accuracy
mp["geometry"] = (
    mp.to_crs(mp.estimate_utm_crs()).simplify(50).to_crs(mp.crs)
)
# Create choropleth map
fig = px.choropleth(df,
                    locations="CDUID",
                    geojson=mp,
                    featureidkey="properties.CDUID",
                    color="category",
                    color_discrete_map={
                        '0': '#fffcfc',
                        '1' : '#ff9e9e',
                        '-1' : '#ff0d0d'},
                    category_orders={
                      'category' : [
                          '0',
                          '1', 
                          '-1'
                      ]
                    },
                    animation_frame="year",
                    scope='north america',
                    title='<b>COVID-19 cases in Canadian provinces</b>',
                    locationmode='geojson-id',
                    )
print("here1")
# Adjust map layout stylings
fig.update_layout(
    showlegend=True,
    legend_title_text='<b>Total Number of Cases</b>',
    font={"size": 16, "color": "#808080", "family" : "calibri"},
    margin={"r":0,"t":40,"l":0,"b":0},
    legend=dict(orientation='v'),
    geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#e0fffe')
)
print("here2")
# Adjust map geo options
fig.update_geos(showcountries=False, showcoastlines=False,
                showland=False, fitbounds="locations",
                subunitcolor='white')
fig.show()
