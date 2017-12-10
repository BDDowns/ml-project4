'''
Data Handler preprocesses data for clustering experiments
'''

import numpy as np
import pandas as pd



class DataHandler():
    def __init__(self):
        pass

def handleCSV(self, file):
    df = pd.read_csv(file)
    return df
@classmethod
def data_to_points(self, file):
    points = []
    df = pd.read_csv(file).as_matrix()
    for i in range(0, len(df)):
        point = DataPoints(df[i])
        points.append(point)
    return points


class DataPoints:
    def __init__(self, attr):
        self.data = attr
        self.loc = [None, None]
        self.clusterlabel = None