import numpy as np
import matplotlib.pyplot as plt
class Printer:
    @staticmethod
    def print_clusters(X, title):
        fig = plt.figure()
        for each in X:
            plt.scatter(each[0], each[1], c='k')
        file_name = "{}.png".format(title)
        fig.savefig(file_name)
        plt.close(fig)
