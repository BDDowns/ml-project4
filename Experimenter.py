'''
Experimenter.py is a driver class that intiates 25 experiments using 5 data sets clustered
with 5 algorithms
'''
import Clustering as cluster
cl = cluster.Clustering()
'''
get_data relies on the external class datahandler to read in csv files of the 5 datasets
used in the experiments. 
'''
def get_data():
    pass

'''
qac_exp executes a quick ant-colony optimization experiment
'''
def qac_exp():
    cl.aco('data/user_knowledge.csv', num_ants=30, iterations=300, board_dim=60)
    cl.aco('data/Anuran calls.csv', num_ants=90, iterations=300, board_dim=150)
    cl.aco('data/seeds.csv', num_ants=25, iterations=300, board_dim=50)
    cl.aco('data/Sales_transactions.csv', num_ants=25, iterations=300, board_dim=50)
    cl.aco('data/movement_libras.csv', num_ants=20, iterations=300, board_dim=35)



'''
hpso_exp executes a hierarchical pso clustering experiment 
'''
def hpso_exp():
    pass

'''
dbscan_exp executes a dbscan clustering experiment
'''
def dbscan_exp():
    pass

'''
kmeans_exp executes a kmeans clustering experiment
'''
def kmeans_exp():
    pass

'''
cnn_exp executes a competative neural network experiment
'''
def cnn_exp():
    pass

qac_exp()