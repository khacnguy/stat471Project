import sqlite3
import pandas as pd
import numpy as np

# Calculate parameters for linear models using maximum likelihood estimation
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

def calculate_parameters(data):
    # data is a list of (p,q,r) triples
    n=len(data)

    # Calculating values of summation for p,q,r
    p_sum=sum([triple[0] for triple in data])
    q_sum=sum([triple[1] for triple in data])
    r_sum=sum([triple[2] for triple in data])
    # Calculating values of summation of squares for p,q,r
    p_sqsum=sum([triple[0]**2 for triple in data])
    q_sqsum=sum([triple[1]**2 for triple in data])
    r_sqsum=sum([triple[2]**2 for triple in data])
    # Calculting summation of prodcuts of pq, pr and qr
    pq_sum=0
    pr_sum=0
    qr_sum=0
    for i in range(0,n):
        pq_sum+=data[i][0]*data[i][1]
        pr_sum+=data[i][0]*data[i][2]
        qr_sum+=data[i][1]*data[i][2]
    
    # Initializing matrix A
    para_matrix=np.array([[p_sqsum,pq_sum,p_sum],[pq_sum,q_sqsum,q_sum],[p_sum,q_sum,n]])
    # Finding inverse of matrix A
    inv = np.linalg.inv(para_matrix)

    # Initializing vector B
    z_vector=np.array([[pr_sum],[qr_sum],[r_sum]])
    
    # Multiply inverse of A with B to find vector of estimated parameters a,b,c
    res= inv.dot(z_vector)
    print(res)
    return res

def sigmoid(a, c, x):
    return a*(1/(1+np.exp(-c*x)) - 1/2)


def main():
    connect("database.db")
    #ax + by + c = ?
    data = get_data()
    data1 = []
    for x in data:
        data1.append(x[:2] + x[3:])
    a, b, c = calculate_parameters(data1)
    real_rental_price = []
    rental_price1 = []
    rental_price2 = []

    for data_point in data:
        real_rental_price.append(data_point[3])
        rental_price1.append(data_point[0] * a[0] + data_point[1]*b[0] + c[0])
        rental_price2.append(sigmoid(500,0.75, data_point[2]))
    
    last_model_data = np.array([rental_price1, rental_price2, real_rental_price]).T
    a1,b1,c1 = calculate_parameters(last_model_data)
    
if __name__ == '__main__':
    main()