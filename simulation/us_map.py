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
        tmp = {"year": year, "category": data[year][location], "CODE": location[-2:]}
        data_reformat.append(tmp)
df = pd.DataFrame(data_reformat)
print(df)


# Create choropleth map
fig = px.choropleth(df,
                    locations="CODE",
                    featureidkey="properties.CODE",
                    color="category",
                    color_discrete_map={
                        '-1' : '#ff0d0d',
                        '0': '#fffcfc',
                        '1' : '#ff9e9e'
                        },
                    category_orders={
                      'category' : [
                          '-1',
                          '0',
                          '1'
                      ]
                    },
                    animation_frame="year",
                    scope='north america',
                    title='<b>COVID-19 cases in Canadian provinces</b>',
                    locationmode='USA-states',
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