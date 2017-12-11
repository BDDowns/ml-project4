'''
Data Handler preprocesses data for clustering experiments
'''

import numpy as np
import pandas as pd



class DataHandler():
    def __init__(self):
        pass

    def handleCSV(self, file):
        df = pd.read_csv(file, header=None)
        return df
    @staticmethod
    def data_to_points(file_name):
        points = []
        df = pd.read_csv(file_name).as_matrix()
        for i in range(0, len(df)):
            point = DataPoints(df[i])
            points.append(point)
        return points
    @staticmethod
    def points_to_dataframe(points):
        base = points[0]
        base = np.asarray([base[0], base[1]])
        for each in points:
            a = np.asarray(each)
            each = np.asarray([each[0], each[1]])
            base = np.vstack((base, each))
        df = pd.DataFrame(data=base)
        return df



class DataPoints:
    def __init__(self, attr):
        self.data = attr
        self.loc = [None, None]
        self.clusterlabel = None