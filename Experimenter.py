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
    #cl.aco('data/user_knowledge.csv', num_ants=90, iterations=300, board_dim=200)
    #cl.aco('data/Anuran calls.csv', num_ants=75, iterations=250, board_dim=340)
    cl.aco('data/seeds.csv', num_ants=50, iterations=250, board_dim=200)
    cl.aco('data/Sales_transactions.csv', num_ants=40, iterations=250, board_dim=200)
    cl.aco('data/movement_libras.csv', num_ants=40, iterations=250, board_dim=200)



'''
hpso_exp executes a hierarchical pso clustering experiment 
'''
def hpso_exp():
    pass

'''
dbscan_exp executes a dbscan clustering experiment
'''
def dbscan_exp():
    cl.dbscan('./data/seeds.csv', 0.5, 5, 'seeds_dbscan')
    cl.dbscan('./data/User_knowledge.csv', 0.2, 25, 'user_knowledge_dbscan')
    cl.dbscan('./data/Sales_Transactions.csv', 1, 25, 'sales_transactions_dbscan')
    cl.dbscan('movement_libras.csv', 0.5, 25, 'movement_libras_dbscan')
    cl.dbscan('./data/Anuran calls.csv', 5, 500, 'anuran_calls_dbscan')

'''
kmeans_exp executes a kmeans clustering experiment
'''
def kmeans_exp():
    cl.kmeans('./data/seeds.csv', 5, 1000, 'seeds_kmeans')

'''
cnn_exp executes a competative neural network experiment
'''
def cnn_exp():
    pass

# qac_exp()
# dbscan_exp()
# kmeans_exp()