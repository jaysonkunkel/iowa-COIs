import numpy as np
import networkx as nx
from queue import Queue
import json
import pickle

# initialize graph of given size
def init_graph(size):
    G = nx.Graph()
    for i in range(size):
        G.add_node(i)
    return G

# add edges to graph
# edges between neighboring tracts only
def add_edges(dict, G):
    for i in dict["tracts"]:
        for j in dict["tracts"]:
            if i['GEOID'] in j['GID_NEIGHB']:
                G.add_edge(i['ID'], j['ID'])

# breadth first search on graph G starting from node start
def bfs(start, G, mat):

    # no nodes visited initally
    visited = np.zeros(size, dtype=bool)
    # arbitrary distances of infinity
    dists = np.full(size, np.inf)
    # initialize empty queue
    q = Queue(maxsize=size)

    q.put(start)
    visited[start] = True
    dists[start] = 0
    mat[start, start] = 0

    while(q.empty() == False):
        v = q.get()
        neighbors = G.adj[v]
        for n in neighbors:
            if(visited[n] == False):
                visited[n] = True
                dists[n] = dists[v] + 1
                mat[start, n] = dists[n]
                mat[n, start] = dists[n]
                q.put(n)  

# loop over all nodes in graph G
def allbfs(G, mat):
    for node in G.nodes():
        bfs(node, G, mat)

#-----------------------begin main code----------------------------#
# suppress scientific notation for console output
np.set_printoptions(suppress=True)

# this is the JSON file with combined tract geography and census data
input = 'C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\shapefiles\\tl_2022_19_tract_ss_2.json'
# input = 'C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\shapefiles\\tl_2022_19_tabblock20.json'

# will hold the all-to-all distance matrix
output = "C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\tract_dists.txt"
# output = "C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\block_dists.txt"

file = open(input)
tract_json = json.load(file)

# i talk about this in the readme
size = len(tract_json["tracts"])
# print("Size: " + str(size))

# N x N matrix to hold all-to-all dists
mat = np.zeros([size, size], dtype=np.int8)

tract_graph = init_graph(size)
add_edges(tract_json, tract_graph)
allbfs(tract_graph, mat)
# print(mat)

# default for savetxt and readtxt is float, so use %i for ints
np.savetxt(output, mat, fmt="%i")

pickle.dump(tract_graph, open('.\\tract_graph.pickle', 'wb'))
#-----------------------end main code----------------------------#


# testing

# test graph
# G = nx.Graph()
# G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7])
# G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4),
#                   (1, 2),
#                   (2, 4), (2, 5), (2, 6),
#                   (3, 4), (3, 7),
#                   (4, 6), (4, 7),
#                   (5, 6)])

# print the population of each census tract
# for i in range(size):
#     newrow = [dict["tracts"][i]["ID"], dict["tracts"][i]["DP02_0124E"]]
#     A[i] = newrow

# i think this is for blocks
# for i in dict:
#     for j in dict:
#         if i['GEOID20'] in j['GID_NEIGHB']:
#             G.add_edge(i['ID'], j['ID'])



 