import sqlite3
import pandas as pd

def connect(path):
    global connection, cursor
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    except sqlite3.Error as error:
        print("error connecting", error)


df = pd.read_csv("csi,pd.csv")
print(len(df))
df = df[df["population_density"].notna()]
df = df[df["population_density"] != "#REF!"]


prov_dict = {
    "ON": "Ontario",
    "QC": "Quebec",
    "AB": "Alberta",
    "MB": "Manitoba",
    "BC": "British Columbia",
    "SK": "Saskatchewan",
    "NL": "Newfoundland and Labrador",
    "NB": "New Brunswick",
    "PEI": "Prince Edward Island"
}
rental_price = []
csi = []
population_density = []
connect("database.db")
for _,rows in df.iterrows():
    string = rows[0] + ", " + prov_dict[rows[1]]
    cursor.execute(
        '''
            SELECT * FROM rp_diff
            WHERE year = 2021
            AND location = (?)
        ;''', (string,)
    )
    ans = cursor.fetchall()
    if len(ans) > 0:
        print(ans)
        rental_price.append(float(ans[0][2]))
        csi.append(float(rows[2]))
        population_density.append(float(rows[3].replace(",", "")))
    
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
 
fig = plt.figure()
 
# syntax for 3-D projection
ax = plt.axes(projection ='3d')
 
# plotting
ax.scatter(rental_price, csi, population_density, 'green')
plt.show()
