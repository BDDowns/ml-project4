'''
Clustering.py Performs experiments using 5 clustering algorithms on 5 data sets
for a total of 25 experiments. 
'''

import pandas as pd
import numpy as np
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
    kmeans performs a clustering of data using the kmeans algorithm
    @param data: (pandas dataframe object) with class labels in last column
           k: (int) number of clusters/centroids
           iters: (int) number of cluster iterations
    @return data: (pandas dataframe object) cluster labeled
    '''
    def kmeans(self, data, k, iters):
        # create a cluster column
        data['cluster'] = np.empty((len(data), 0)).tolist()
        count = 0
        while count < iters:
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