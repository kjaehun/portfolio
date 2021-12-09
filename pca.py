## Principal Component Analysis
## 09/28/2021

## image compression using PCA
## used part of the Yale face dataset: 2414 sample images, each of size 32x32

import scipy.linalg
from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

## load the dataset from a provided .npy file, re-center it around the origin
##      and return it as a NumPy array of floats
def load_and_center_dataset(filename):
    x = np.load(filename)
    return x - np.mean(x, axis=0) 
    
## calculate and return the covariance matrix of the dataset
##      as a NumPy matrix (d x d array)
def get_covariance(dataset):
    x = dataset
    return (np.dot(np.transpose(x), x)) / (len(dataset) - 1)

## perform eigen decomposition on the covariance matrix S and return a diagonal
##      matrix with the largest m eigenvalues on the diagonal, and a matrix
##      with the corresponding eigenvectors as columns
def get_eig(S, m):
    x = scipy.linalg.eigh(S, eigvals=(len(S)-m, len(S)-1))
    evals = x[0]
    evecs = x[1]
    evals = evals[::-1]
    diag = np.diag(evals)
    evecs = np.fliplr(evecs)
    return diag, evecs
    
## similar to get_eig, but instead of returning the first m, return all eigenvalues
##      and corresponding eigenvectors in similar format as get_eig that
##      explain more than perc % of variance
## ex: if perc is 0.05, return all the eigenvalues/eigenvectors that explain more than 0.05 % of variance
def get_eig_perc(S, perc):
    x = scipy.linalg.eigh(S)
    evals = x[0]
    evecs = x[1]
    evals = evals[::-1]
    evecs = np.fliplr(evecs)
    evalSum = np.sum(evals)
    newevals = np.empty([0,1])
    newevecs = np.empty([0,len(evecs)])
    i,n = 0, 0
    for evl in evals:
        if (evl/evalSum) > perc:
            newevals = np.append(newevals, evl)
            newevecs = np.vstack((newevecs, evecs[:,i]))
            n += 1
        i += 1

    diag = np.diag(newevals)
    newevecs = np.transpose(newevecs)
    return diag, newevecs

## project each image into your m-dimensional space
##      and return the new representation as a d x 1 NumPy array
def project_image(img, U):
    n = len(U[0])
    proj = np.zeros(len(img))
    for i in range(0, n):
        a = np.dot(np.transpose(U[:,i]), img)
        proj = np.add(proj, np.multiply(a, U[:,i]))
    return proj

## display a visual representation of the original image
##      and the projected image side-by-side
def display_image(orig, proj):
    a = np.transpose(np.reshape(orig, (32,32)))
    b = np.transpose(np.reshape(proj, (32,32)))
    fig, (left, right) = plt.subplots(1, 2)
    left.set_title('Original')
    right.set_title('Projection')
    l = left.imshow(a, aspect='equal')
    r = right.imshow(b, aspect='equal')
    fig.colorbar(l, ax=left)
    fig.colorbar(r, ax=right)
    plt.show()

## sample usage:
## x = load_and_center_dataset('images.npy')
## S = get_covariance(x)
## Lambda, U = get_eig(S, 2)
## projection = project_image(x[0], U)
## display_image(x[0], projection)
