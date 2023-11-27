import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sqlite3 

def sigmoid(x, x0, k):
    y = 1 / (1 + np.exp(-k*(x-x0)))
    return y
def GD(xdata, ydata):
    print(ydata.mean(), ydata.std())
    ydata = ((ydata - np.average(ydata)) / ydata.std())
    print(ydata)
    print(xdata.mean(), ydata.mean(), xdata.std(), ydata.std())


    popt, pcov = curve_fit(sigmoid, xdata, ydata)
    print(popt)
    x = np.linspace(-2.5, 2.9, 50)
    y = sigmoid(x, popt[0], popt[1])





    plt.plot(xdata, ydata, 'o', label='RI01_activity', color='blue')
    plt.plot(x, y, label='fit_activity')
    plt.ylim(-0.1, 1.2)
    plt.legend(loc='best')
    plt.show()
def connect(path):
    global connection, cursor
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
    except sqlite3.Error as error:
        print("error connecting", error)

def get_data():
    cursor.execute('''
        SELECT population_density, cnt, val_diff, price_diff FROM final_data_diff
    ;''')
    return cursor.fetchall()

def main():
    connect("database.db")
    data = get_data()
    X = np.array([x[2] for x in data])
    Y = np.array([x[3] for x in data])
    y_mean = Y.mean()
    y_std = Y.std()
    print(y_mean, y_std)
    Y=np.array((Y-Y.mean())/Y.std())
    x_mean = X.mean()
    x_std = X.std()
    X=np.array((X-X.mean())/X.std())
    GD(X,Y)
main()