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

def data_to_points(self, file):
    points = []
    df = pd.read_csv(file).as_matrix()


class DataPoints:
    def __init__(self, attr):
        self.data = attr
        self.loc = [None, None]
        self.clusterlabel = None
        self.carrier = None
    def set_down(self):
        self.loc = self.carrier.pos
        self.carrier = None
    def pick_up(self, ant):
        self.carrier = ant
        self.loc = [None, None]