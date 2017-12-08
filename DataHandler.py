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