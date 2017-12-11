import Clustering as cluster
cl = cluster.Clustering()
cl.aco('data/seeds.csv', num_ants=30, iterations=120, board_dim=120)