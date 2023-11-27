import numpy as np
import math
import sqlite3 
def simulate_data(mu, sigma, n):
    sim = np.random.normal(loc = mu, scale = sigma, size = n)
    return sim

def sigmoid(a, c, x):
    return a*(1/(1+np.exp(-c*x)) - 1/2)

def inverse(a, c, rental_price):
    return np.log(1/(rental_price/a + 1/2) - 1)/-c

def main():
    data = get_data()
    rental_price = [x[3] for x in data]
    print(rental_price)
    samples = len(rental_price)
    sim = simulate_data(0, 1, samples)
    simulated = []
    for sample in range(samples):
        simulated.append(inverse(500,0.75,rental_price[sample] - sim[sample]))
        print(simulated[sample], data[sample][2])
    for i in range (samples):
        cursor.execute('''
            UPDATE final_data_diff
            SET val_diff = (?)
            WHERE year = (?) AND location = (?) AND DGUID = (?)
        ;''', (simulated[i], data[i][4], data[i][5], data[i][6]))
    connection.commit()
def connect(path):
    global connection, cursor
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    except sqlite3.Error as error:
        print("error connecting", error)

def get_data():
    cursor.execute('''
        SELECT population_density, cnt, val_diff, price_diff, year, location, DGUID  FROM final_data_diff
    ;''')
    return cursor.fetchall()
if __name__ == '__main__':
    connect("database.db")
    main()