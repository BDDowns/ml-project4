'''
Clustering.py Performs experiments using 5 clustering algorithms on 5 data sets
for a total of 25 experiments. 
'''

import pandas as pd
import numpy as np
import random as rn

class Clustering():
    def __init__(self):
        pass


'''
dbscan performs a clustering of data using the DBSCAN algorithm
@param data: (pandas dataframe object) with class labels in last column
       eps: (float) the minimum distance between points in a cluster 
       minPts: (integer) the minimum number of points to constitute a cluster
@return data: (pandas dataframe object) with cluster labels added to the last column
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
            for i in seeds:
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
kmeans performs a clustering of data using a variation of Lloyd's kmeans algorithm
Andrew Ng pseudocode from http://stanford.edu/~cpiech/cs221/handouts/kmeans.html referenced
@param data: (pandas dataframe object) with class labels in last column
       k: (int) number of clusters/centroids
       iters: (int) number of cluster iterations
@return data: (pandas dataframe object) cluster labeled 
'''
def kmeans(self, data, k, max_iters):
    # create a cluster column
    data['cluster'] = np.empty((len(data), 0)).tolist()
    count = 0
    self.MAX_ITERATIONS = max_iters
    # intialize k cluster centers arbitrarily
    centroids = self.get_k_centroids(data, k)
    oldCentroids = None
    while not self.stop_cluster(oldCentroids, centroids, count):
        # do kmeans stuff
        oldCentroids = centroids
        count += 1
        # label according to closest centroid
        data = self.assign_labels(data, centroids)
        # compute new centroids
        centroids = self.update_centroids(data, centroids)


'''
stop clustering if max iterations exceeded, or centroids no longer change
'''
def stop_cluster(self, oldCentroids, centroids, count):
    if count > self.MAX_ITERATIONS: 
        return True
    return oldCentroids == centroids

'''
get_k_random_centroids is used to initialize k random centroids by index from 0 to len(data)
@param data: (pandas dataframe object)
       k: (int) number of centroids
@return (list) of data objects
'''
def get_k_random_centroids(self, data, k):
    indeces = rn.sample(range(0, len(data)), k)
    centroids = []
    for i in indeces:
        centroids.append(data[i])
    return centroids

def update_centroids(self, data, centroids):
    # iterate over the dataset and calculate geometric mean for each center type
    for i in range(len(centroids)):
        number_in_cluster = 1
        for index, row in data.iterrows():
            # sum attributes of like clusters and divide by number of matches
            if row['cluster'] == i:
                number_in_cluster += 1
                for j in range(len(row) - 2):
                    centroids[j][i] += row[j]
        # compute geometric mean
        for j in range(len(centroids.loc[0]) - 2):
            centroids.loc[j] = centroids.loc[j] / number_in_cluster
    return centroids

def assign_labels(self, data, centroids):
    # loop over all data in dataset
    for index, row in data.interrows():
        distOld = 999999999
        dist = distOld
        # loop over all centroids known
        for i in range(len(centroids)):
            dist = min(dist, self.euclidian_d(centroids[i], row))
            if dist < distOld:
                data.loc[index, 'cluster'] = i
            distOld = dist

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