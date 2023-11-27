import sqlite3
import pandas as pd

#cleaning and loading data for simulation
def connect(path):
    global connection, cursor
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    except sqlite3.Error as error:
        print("error connecting", error)

def load_rental_price():
    rental_price = pd.read_csv('load_data/data/rental_price.csv')
    rental_price = rental_price[rental_price['VALUE'].notna()]
    rental_price = rental_price[rental_price['DGUID'].notna()]

    rental_price = rental_price.drop(['UOM', 'UOM_ID', 'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS', 'COORDINATE', 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR'], axis = 1)
    for row in rental_price.iterrows():
        cursor.execute('''INSERT INTO rental_price VALUES (?,?,?,?,?,?);''', row[1])
    connection.commit()

def new_location(location):
    lol = ["Ontario","Quebec","Alberta","Manitoba", "British Columbia", "Saskatchewan"]
    for loc in lol:
        if loc in location:
            return location[0:location.find(loc) + len(loc)]

def load_csi():
    for prov in ["AB", "BC", "MA", "ON", "QB", "SA"]:
        homicide_rates = pd.read_csv("load_data/data/csi/" + prov + '.csv')
        homicide_rates = homicide_rates[homicide_rates['VALUE'].notna()]
        homicide_rates = homicide_rates[homicide_rates['VALUE'] != 0.0]
        homicide_rates = homicide_rates.drop(['UOM', 'UOM_ID', 'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS', 'COORDINATE', 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR', 'Statistics'], axis = 1)
        for row in homicide_rates.iterrows():
            if row[1][2] != 0.0:
                cursor.execute('''INSERT INTO csi VALUES (?,?,?,?);''', (row[1][0], new_location(row[1][1]), row[1][2], row[1][3]))
    connection.commit() 

def load_population():
    population = pd.read_csv('load_data/data/population.csv')
    population = population[population['VALUE'].notna()]
    population = population[population['DGUID'].notna()]
    population = population.drop(['Sex', 'Age group', 'UOM', 'UOM_ID', 'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS', 'COORDINATE', 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR'], axis = 1)
    for row in population.iterrows():
        cursor.execute('''INSERT INTO population VALUES (?,?,?,?);''', (row[1][0], row[1][1].replace(' (CMA)', '').replace(' (CA)', ''), row[1][2], row[1][3]))
    connection.commit() 

def load_er():
    gdp = pd.read_csv('load_data/data/employment_rate.csv')
    for row in gdp.iterrows():
        for year in range(2006,2023):
            cursor.execute('''INSERT INTO employment_rate VALUES (?,?,?);''', (year, row[1]["GEO"], row[1][str(year) + "-09"]))
    connection.commit() 

def load_area():
    area = pd.read_csv("load_data/data/area.csv")
    for _,row in area.iterrows():
        location = row["Municipality"] + ", " + row["Province"]
        cursor.execute('''INSERT INTO area VALUES (?,?);''', (location, row["Land area (km2)"]))
    connection.commit() 

if __name__ == '__main__':
    connect("database.db")
    load_rental_price()
    load_csi()
    load_population()
    load_er()
    load_area()

