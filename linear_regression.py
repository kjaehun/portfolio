## Linear Regression
## 10/22/2021

import numpy as np
from matplotlib import pyplot as plt
import csv
import math

## csv format: 16 features (first is the target, bodyfat percentage), 252 samples
## takes a filename and returns the data as an 252-by-16 array
def get_dataset(filename):
    with open(filename, 'r') as doc:
        reader = csv.reader(doc)
        m = len(next(reader))
        d = np.empty([0, m - 1])
        for row in reader:
            del row[0]
            for i in range(0, len(row)):
                row[i] = float(row[i])
                
            d = np.vstack((d, row))

    return dataset

## takes the dataset produced by get_dataset() and
##      prints several statistics about a column of the dataset; does not return anything
def print_stats(dataset, col):
    c = dataset[:,col]
    n = len(c)
    mean = 0
    std = 0
    for data in c:
        mean += data
    mean /= n
    for data in c:
        std += (data - mean)**2
    std /= (n-1)
    std = math.sqrt(std)
    print(n)
    print('{:.2f}'.format(mean))
    print('{:.2f}'.format(std))

## calculates and returns the mean squared error on the dataset given fixed betas
def regression(dataset, cols, betas):
    n = len(dataset)
    c = len(cols)
    mse = 0
    for i in range(0, n):
        x = betas[0]
        for k in range(0, c):
            x += dataset[:,cols[k]][i] * betas[k+1]
        x -= dataset[i][0]
        mse += x**2

    mse /= n
    
    return mse

## performs a single step of gradient descent on the MSE and returns the derivative values as an 1D array
def gradient_descent(dataset, cols, betas):
    n = len(dataset)
    c = len(cols)
    grads = np.empty(c+1)
    mse = 0
    for i in range(0, n):
        x = betas[0]
        for k in range(0, c):
            x += dataset[:,cols[k]][i] * betas[k+1]
        x -= dataset[i][0]
        mse += x
    mse *= 2
    mse /= n
    grads[0] = mse
    for j in range(1, c+1):
        mse = 0
        for i in range(0, n):
            x = betas[0]
            for k in range(0, c):
                x += dataset[:,cols[k]][i] * betas[k+1]
            x -= dataset[i][0]
            x *= dataset[i][cols[j-1]]
            mse += x
        mse *= 2
        mse /= n
        grads[j] = mse

            
    return grads

## performs T iterations of gradient descent starting at the given betas and prints the results; does not return anything
def iterate_gradient(dataset, cols, betas, T, eta):
    for i in range(1, T+1):
        betas = betas - gradient_descent(dataset, cols,betas)*eta
        mse = regression(dataset, cols, betas)
        print(i, '{:.2f}'.format(mse), end=" ")
        for i in range(len(betas)):
            print('{:.2f}'.format(betas[i]), end=" ")
        print()

## using the closed-form solution, calculates and returns the values of betas and the corresponding MSE as a tuple
def compute_betas(dataset, cols):
    m = len(dataset)
    n = len(cols)
    x = np.empty([m,n+1])
    x[:,0] = 1
    for i in range(1,n+1):
        x[:,i] = dataset[:,cols[i-1]]
    b = np.matmul( np.matmul( np.linalg.inv(np.matmul(np.transpose(x), x) ) , (np.transpose(x)) ), dataset[:,0] )
    mse = regression(dataset, cols, b)
    betas=[]
    betas.append(mse)
    for i in range(0, len(b)):
        betas.append(b[i])
    return tuple(i for i in betas)

## using the closed-form solution betas, return the predicted bodyfat percentage of the given features
def predict(dataset, cols, features):
    n = len(cols)
    b = compute_betas(dataset, cols)
    betas = []
    for i in range(1, n+2):
        betas.append(b[i])
    result = 0
    result += betas[0]
    for i in range(0, n):
        result += features[i] * betas[i+1]
    
    return result

## generates two synthetic datasets, one using a linear model and the other using a quadratic model
def synthetic_datasets(betas, alphas, X, sigma):
    x = X[:,0]
    n = len(x)
    l = np.empty([n,2])
    q = np.empty([n,2])

    for i in range(0, n):
        l[i] = [betas[0] + betas[1] * x[i] + np.random.normal(0, sigma), x[i]]
        q[i] = [(alphas[0] + alphas[1] * x[i]**2 + np.random.normal(0, sigma)), x[i]]

    
    return l, q

## fits the synthetic datasets, and plots a figure depicting the MSEs under different situations
def plot_mse():
    from sys import argv
    if len(argv) == 2 and argv[1] == 'csl':
        import matplotlib
        matplotlib.use('Agg')

    # Generate datasets and plot an MSE-sigma graph
    X = np.reshape(np.linspace(-100, 100, 1000), (1000, 1))
    betas = np.array([-1,2])
    alphas = np.array([1,-2])
    sigmas = []
    for i in range(-4, 6):
        sigmas.append(10**i)
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    plt.xlabel('Sigma')
    ax.set_xscale('log')
    plt.ylabel('MSE of Trained Model')
    ax.set_yscale('log')
    mse1 = np.empty([10,])
    mse2 = np.empty([10,])
    i = 0
    for sigma in sigmas:
        l, q = synthetic_datasets(betas, alphas, X, sigma)
        mse1[i] = compute_betas(l, np.array([1]))[0]
        mse2[i] = compute_betas(q, np.array([1]))[0]
        i += 1
        
    plt.plot(sigmas, mse1, '-ro', label='MSE of Linear Dataset')
    plt.plot(sigmas, mse2, '-bo', label='MSE of Quadratic Dataset')
    plt.legend()
    plt.savefig('mse.pdf')

if __name__ == '__main__':

    plot_mse()
