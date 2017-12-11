'''
Clustering.py Performs experiments using 5 clustering algorithms on 5 data sets
for a total of 25 experiments. 
'''

import pandas as pd
import numpy as np

import random as rn

import DataHandler as dh
import Ants
from sklearn.metrics import calinski_harabaz_score as scorer
from sklearn.preprocessing import LabelEncoder


class Clustering:
    def clustering(self):
        self.handler = dh
    '''
    dbscan performs a clustering of data using the DBSCAN algorithm
    @param data: (pandas dataframe object) with class labels in last column
           eps: (float) the minimum distance between points in a cluster
           minPts: (integer) the minimum number of points to constitute a cluster
    @return data: (pandas dataframe object) with cluster labels added to the last column
    '''
    def dbscan(self, data, eps, minPts, outname):
        data = pd.read_csv(data, header=None)
        # Track number of clusters
        cluster = 0
        # append cluster labels list and initialize to unlabeled
        data['cluster'] = np.empty((len(data), 0)).tolist()
        # loop over datapoints
        for index, row in data.iterrows():
            # only continue if the label is undefined
            if data.loc[index, 'cluster'] == []:
                neighbors = self.range_check(data, row, eps)
                if len(neighbors) < minPts:
                    data.loc[index, 'cluster'] = 'Noise'
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
                                if index not in seeds:
                                    seeds.append(index)
        data.to_csv("./results/{}".format(outname))

    def range_check(self, data, Q, eps):
        neighbors = []
        for index, row in data.iterrows():
            if self.euclidean_d(row, Q) <= eps:
                neighbors.append(index)
        return neighbors

    def euclidean_d(self, a, b):
        distance = 0
        # hand wave magic teim
        # this assumes that a class label was the last column, and we added the empty cluster column...
        for i in range(len(a) - 1):
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
    def kmeans(self, data, k, max_iters, outname):
        data = pd.read_csv(data, header=None)
        # create a cluster column
        data['cluster'] = np.empty((len(data), 0)).tolist()
        count = 0
        self.MAX_ITERATIONS = max_iters
        # intialize k cluster centers arbitrarily
        centroids = self.get_k_random_centroids(data, k)
        oldCentroids = None
        while not self.stop_cluster(oldCentroids, centroids, count):
            # do kmeans stuff
            oldCentroids = centroids
            count += 1
            # label according to closest centroid
            data = self.assign_labels(data, centroids)
            # compute new centroids
            centroids = self.update_centroids(data, centroids)
        data.to_csv('./results/{}'.format(outname))

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
            centroids.append(data.loc[i])
        return centroids

    def update_centroids(self, data, centroids):
        # iterate over the dataset and calculate geometric mean for each center type
        for i in range(len(centroids)):
            number_in_cluster = 1
            for index, row in data.iterrows():
                # sum attributes of like clusters and divide by number of matches
                if data.loc[index, 'cluster'] == i:
                    number_in_cluster += 1
                    for j in range(len(row) - 1):
                        centroids[i][j] += data.loc[index, j]
            # compute geometric mean
            for j in range(len(centroids[0]) - 1):
                centroids[i][j] = centroids[i][j] / number_in_cluster
        return centroids

    def assign_labels(self, data, centroids):
        # loop over all data in dataset
        for index, row in data.iterrows():
            distOld = 999999999
            dist = distOld
            # loop over all centroids known
            for i in range(len(centroids)):
                dist = min(dist, self.euclidean_d(centroids[i], row))
                if dist < distOld:
                    data.loc[index, 'cluster'] = i
                distOld = dist
        return data

    '''
    aco peforms a clustering of input data using the ant colony optomization algorithm
    @param
    @return
    '''

    def aco(self, file_name, num_ants, iterations, board_dim):
        datapoints = dh.DataHandler.data_to_points(file_name)
        file_name = file_name.strip(".csv")
        aco = Ants.AntFarm(num_ants, datapoints, filename=file_name, max_iterations=iterations, dim=board_dim)
        df = dh.DataHandler.points_to_dataframe(aco.run())
        df = self.dbscan(df, 4, 9)
        print("scoring {}\n\n".format(file_name))
        score = self.evaluate_model(df)
        with open("{} score.txt".format(file_name), 'w') as results:
            results.write(str(score))
            results.close()
        print("finished".format(file_name))

    def evaluate_model(self, data):
        le = LabelEncoder()
        #drop non_clustered points from dataframe
        data['cluster'] = data['cluster'].where(data['cluster'].str.len() > 0, np.nan)
        data.dropna(subset=['cluster'], inplace=True)
        #separate cluster labels from datapoints
        points = data.as_matrix(columns=data.columns[1:-1])
        labels = data.as_matrix(columns=data.columns[-1:])
        le.fit_transform(np.ravel(labels))
        labels = le.transform(labels)
        #returns numpy float64 score value
        return scorer(points, labels)

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