import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sqlite3 

# apply gradient descent with synthetic data to find parameters for simulation
DATABASE_PATH = "database.db"

def sigmoid(x, x0, k):
    y = 1 / (1 + np.exp(-k*(x-x0)))
    return y
def GD(xdata, ydata):
    # apply gradient descent to x and y
    print("Average rental price: ", ydata.mean(), "Standard deviation of rental price: ", ydata.std())
    print("Average employment rate change: ", xdata.mean(), "Standard deviation of employment rate change: ", xdata.std())
    ydata = ((ydata - np.average(ydata)) / ydata.std())




    popt, pcov = curve_fit(sigmoid, xdata, ydata)
    print("Parameters in sigmoid function: ", popt)
    x = np.linspace(-2.5, 2.9, 50)
    y = sigmoid(x, popt[0], popt[1])





    plt.plot(xdata, ydata, 'o', label='data', color='blue')
    plt.plot(x, y, label='fit_activity')
    plt.ylim(-0.1, 1.2)
    plt.legend(loc='best')
    plt.show()

def connect(path):
    # connect to database
    global connection, cursor
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    except sqlite3.Error as error:
        print("error connecting", error)

def get_data():
    # get data from database
    cursor.execute('''
        SELECT population_density, cnt, val_diff, price_diff FROM final_data_diff
    ;''')
    return cursor.fetchall()

def main():
    connect(DATABASE_PATH)
    data = get_data()
    # quick data cleaning
    X = np.array([x[2] for x in data])
    Y = np.array([x[3] for x in data])
    y_mean = Y.mean()
    y_std = Y.std()
    Y=np.array((Y-Y.mean())/Y.std())
    x_mean = X.mean()
    x_std = X.std()
    X=np.array((X-X.mean())/X.std())
    
    GD(X,Y)
main()