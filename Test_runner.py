import Clustering as cluster
cl = cluster.Clustering()
cl.aco('data/user_knowledge.csv', num_ants=30, iterations=15)