#!/usr/bin/python
import networkx as nx
import numpy as np
import operator

N13=np.loadtxt('/Users/halehashki/Haleh/Thesis/Paper/codes/data/Eigenvector/N13.txt',delimiter='\t')
G=nx.from_numpy_matrix(N13)
NC13=nx.degree_centrality(G)
print NC13
sorted_x = sorted(NC13.items(), key=operator.itemgetter(1))
print sorted_x
h=nx.closeness_centrality(G)
print h
BC13=nx.betweenness_centrality(G)
print BC13