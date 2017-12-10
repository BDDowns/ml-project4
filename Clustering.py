'''
Clustering.py Performs experiments using 5 clustering algorithms on 5 data sets
for a total of 25 experiments. 
'''

import pandas as pd
import numpy as np

class Clustering():
    def __init__(self):
        pass


'''
dbscan performs a clustering of data using the DBSCAN algorithm
@param data: a pandas dataframe object
       eps: float; the minimum distance between points in a cluster 
       minPts: integer; the minimum number of points to constitute a cluster
@return pandas dataframe object with cluster labels added to the last column
'''
def dbscan(self, data, eps, minPts):
    # Track number of clusters
    cluster = 0
    # append cluster labels list and initialize to unlabeled
    data['cluster'] = np.empty((len(data), 0)).tolist()
    # loop over datapoints
    for index, row in data.iterrows():
        # only continue if the label is undefined
        if row[-1] == []:
            neighbors = self.range_check(data, row, eps)
            if len(neighbors) < minPts:
                row[-1] = "Noise"
                continue
            cluster += 1
            row[-1] = "Cluster " + str(cluster)
            seeds = neighbors
            for i in range(len(seeds)):
                if data.loc[i, 'cluster'] == 'Noise':
                    data.loc[i, 'cluster'] = 'Border ' + str(cluster)
                if data.loc[i, 'cluster'] == []:
                    data.loc[i, 'cluster'] = 'Cluster ' + str(cluster)
                    neighbors = self.range_check(data, data.loc[i], eps)
                    if len(neighbors) >= minPts:
                        for index in neighbors:
                            seeds.append(index)
    return data

def range_check(self, data, Q, eps):
    neighbors = []
    for index, row in data.iterrows():
        if self.euclidian_d(row, Q) <= eps:
            neighbors.append(index)
    return neighbors

def euclidian_d(self, a, b):
    distance = 0
    # hand wave magic teim
    # this assumes that a class label was the last column, and we added the empty cluster column...
    for i in range(len(a) - 2):
        distance += (a[i] - b[i])**2
    return distance

'''
kmeans performs a clustering of data using the kmeans algorithm
@param
@return
'''
def kmeans(self):
    pass


'''
complearning performs a clustering of input data using competative learning neural networks
@param
@return
'''
def complearning(self):
    pass


'''
aco peforms a clustering of input data using the ant colony optomization algorithm
@param
@return
'''
def aco(self):
    pass


'''
pso performs a clustering of input date using particle swarm optimization
@param
@return
'''
def pso(self):
    pass


'''
printplots outputs an <n dimensional> projection of clustered data
@param
@return
'''
def printplots(self):
    pass