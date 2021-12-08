## Clustering
## 10/12/2021

## Simulate SciPy's hierarchical agglomerative clustering function, linkage()

import csv
import numpy as np
from scipy.spatial.distance import pdist, squareform
import random
import matplotlib.pyplot as plt
import math

## generate a list of randomly generated 2D coordinates
## returns a list of tuples
def random_x_y(m):
    a = []
    for i in range(0, m):
        a.append((random.randint(1,359), random.randint(1,359)))
    return a

## performs clustering, displays each linkage being made, and prints information on each clustering
def imshow_hac(dataset):
    m = len(dataset)
    a = np.array(dataset)
    colors = np.random.rand(m)
    plt.scatter(a[:,0], a[:,1], c=colors)
    dists = pdist(a)
    for i in range(0, len(dists)):
        if dists[i]==0:
            dists[i]=-1 # ignore if distance is zero
    dmatrix = squareform(dists)
    ## shape of dmatrix should be (m, m)

    activeClusters = {}
    for i in range(0, m):
        activeClusters[i] = [i]
    ## initially, each point is its own cluster and there are m initial clusters
        
    z = np.empty([m-1, 4]) # need m-1 linkings to fully connect m points
    ## i-th row of Z contains information on the clusters you combined at the i-th iteration
    ## 0th and 1st columns contain the linked clusters
    ## 2nd column contains the Euclidean distance between the newly linked clusters of that iteration
    ## 3rd column contains the number of points in the newly formed cluster
    r = 0
    for row in z:
        beforep = 10000
        beforeq = 10000
        sameCluster = True
        while sameCluster:
            dmin = np.amin(dists) ## find next shortest distance
            dists = np.delete(dists, [np.argmin(dists)])
            ## iterate through dmatrix to find which points created dmin
            for x in range(0, m):
                for y in range(0, m):
                    if dmatrix[x][y]==dmin:
                        t=x
                        s=y
                        for k in activeClusters:
                            if x in activeClusters[k]:
                                p = k
                            if y in activeClusters[k]:
                                q = k
                        ## p, q are our tentative clusters to be linked
                        ## want smaller clusters to be listed first
                        if p > q:
                            temp = p
                            p = q
                            q = temp
                            temp = t
                            t = s
                            s = temp

## tie - breaking: if there are multiple pairs of clusters that have equal distances,
## choose the pair with the smallest first cluster index (p)
## if still tied, then choose the pair with the smallest second cluster index (q)
                        if p!=q and p<beforep:
                            finalp=p
                            finalq=q
                            sameCluster = False
                            finalt = t
                            finals = s
                            beforep = p
                            beforeq = q
                        elif p!=q and p==beforep and q<beforeq:
                            finalp=p
                            finalq=q
                            sameCluster = False
                            finalt = t
                            finals = s
                            beforep = p
                            beforeq = q

        ## add new cluster to activeClusters and remove linked clusters
        activeClusters[m+r] = activeClusters[finalp] + activeClusters[finalq]
        activeClusters.pop(finalp)
        activeClusters.pop(finalq)
        z[r] =[finalp, finalq, dmin, len(activeClusters[m+r])]
        r += 1

        ## display points being linked with a 0.1 second interval
        plt.plot([a[finalt][0], a[finals][0]], [a[finalt][1], a[finals][1]])
        plt.pause(0.1)

    print(z)
    plt.show()
