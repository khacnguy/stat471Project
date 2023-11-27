from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import math
import sqlite3 

def generateXvector(X):
    """ Taking the original independent variables matrix and add a row of 1 which corresponds to x_0
        Parameters:
          X:  independent variables matrix
        Return value: the matrix that contains all the values in the dataset, not include the outcomes variables. 
    """
    vectorX = np.c_[np.ones((len(X), 1)), X]
    return vectorX

def theta_init(X):
    """ Generate an initial value of vector θ from the original independent variables matrix
         Parameters:
          X:  independent variables matrix
        Return value: a vector of theta filled with initial guess
    """
    theta = np.random.randn(len(X[0])+1, 1)
    return theta

def Multivariable_Linear_Regression(X,Y,learningrate, iterations):
    """ Find the multivarite regression model for the data set
         Parameters:
          X: independent variables matrix
          y: dependent variables matrix
          learningrate: learningrate of Gradient Descent
          iterations: the number of iterations
        Return value: the final theta vector and the plot of cost function
    """
    #X is list of employment_rate
    #Y is list of rental_price
    sigma = np.std(X)
    #reshape
    X = np.reshape(X,(len(X[0]),1))
    Y = np.reshape(Y,(len(Y[0]),1))
    m = len(X)
    #change X,y to np.array
    cost_lst = []
    a,c = np.random.rand(2)
    y_pred = np.zeros((m,1))
    for i in range(iterations):
        if i%100 == 0:
            print(i)
        #find Jacobian(we have already)
        #same
        a += learningrate * sigmoid_da(a,c,X,Y,sigma,m)
        c += learningrate * sigmoid_dc(a,c,X,Y,sigma,m)

        #predict from X
        for j in range(m):
            #a,b,c = theta...
            y_pred[j][0] = sigmoid(X[j][0],a,c)

        cost_value = y_pred - Y
        #Calculate the loss for each training instance
        total = 0
        for j in range(m):
            total += abs(cost_value[j][0])
            #Calculate the cost function for each iteration
        cost_lst.append(total)
        print(total)
    plt.scatter(range(1000), cost_lst, color = 'red')
    plt.title('Cost function Graph')
    plt.xlabel('Number of iterations')
    plt.ylabel('Cost')
    return a,c

def sigmoid(a, c, x):
    return a*(1/(1+np.exp(-c*x)) - 1/2)

def sigmoid_da(a, c, x, y, sigma,n):
    sum = 0
    for i in range(n):
        sum += (y[i][0] - sigmoid(a, c, x[i][0]))*(1/(1+np.exp(-c*x[i][0])) - 1/2)
    sum *= -1/sigma**2
    return sum

def sigmoid_dc(a, c, x, y, sigma,n):
    sum = 0
    for i in range(n):
        sum += (y[i][0] - sigmoid(a, c, x[i][0]))*((-x[i][0]*np.exp(-c*x[i][0]))/(1+np.exp(-c*x[i][0]))**2)
    sum *= -a/sigma**2
    return sum
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
    X = np.array([[x[2] for x in data]])
    Y = np.array([[x[3] for x in data]])
    y_mean = Y.mean()
    y_std = Y.std()
    print(y_mean, y_std)
    print((Y[0][0] - y_mean )/y_std)
    Y=np.array((Y-Y.mean())/Y.std())
    print(Y[0][0])
    x_mean = X.mean()
    x_std = X.std()
    X=np.array((X-X.mean())/X.std())

    

    print(Multivariable_Linear_Regression(X,Y, 0.001, 1000))
    plt.show()


if __name__ == '__main__':
    main()
    

