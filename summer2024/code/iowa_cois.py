import numpy as np
import networkx as nx
from networkx import Graph
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt
import csv
from flatclustering_census import size
from flatclustering_mhd import num_flatclusters
import json
import pandas as pd

# this is step 2
# step 1 is flatclustering_mhd.py

# read matrix from file
# distances between all tracts
input = "./summer2024/util/tract_dists.txt"
tract_dists = np.loadtxt(input)

with open('./summer2024/util/clusters_tracts.csv', 'r') as file:
  csv_reader = csv.reader(file)
  clusters = list(csv_reader)

# maps geoids to an index 0 to n-1
with open('./summer2024/util/geoid_index.json', 'r') as file:
  geoids = json.load(file)

# print(flatclusters)

# unsure of size needed
# tracts_in_regions = np.zeros([size, 3], dtype=np.int16)

# for i in range(len(flatclusters)):
#     fc_num = flatclusters[i, 1]
#     tracts_in_flatclusters = clusters[i][2].split()
#     for geoid in tracts_in_flatclusters:
#         j = geoids.get(geoid)
#         tracts_in_regions[j] = [j, fc_num, tracts_in_regions[j][2] + 1]

# data = []
# for i in range(len(flatclusters)):
#     tracts_in_flatclusters = clusters[i][2].split()
#     for geoid in tracts_in_flatclusters:
#        j = geoids.get(geoid)
#        newrow = [j, flatclusters[i, 1],]

# indices = [i for i, x, y in enumerate(flatclusters) if y == 0]
# print("Indices", indices)

# **
# S = map(int, set(flatclusters[:,1]))
# for row in S:
#   print(row)

#---------------------------------------------------#
# # **begin individual symbology

# # i'm only checking a specific cluster
# # reminder to look for region-1 in flatclusters because the regions dont have a 0-indexed column in the csv file
# test = 65

# # this will hold every region marked as cluster "test"
# regions = []

# # generate the list of regions in cluster "test"
# for row in flatclusters:
#   if row[1] == test:
#     regions.append(int(row[0]))

# # this will hold all of the tracts from all regions in "test"
# all_tracts = []

# # clusters[region][2] is the list of tracts in a given number
# for region in regions:
#   for tracts in clusters[region][2].split():
#     all_tracts.append(tracts)

# # get a list of unique tracts 
# set_all_tracts = list(set(all_tracts))

# # this is the np array that will become the file
# tracts_in_regions = np.zeros([len(set_all_tracts), 3], dtype=np.int16)

# # for each unique tract
# for i in range(len(set_all_tracts)):
#   current = set_all_tracts[i]

#   # first column - given a GEOID, what is the tract id? geoids holds the mapping from geoid to ID
#   tracts_in_regions[i][0] = geoids.get(current)
#   # second column is simply the cluster number, "test"
#   tracts_in_regions[i][1] = test
#   # go through list of all census tracts and count how many times a unique tract appears
#   for j in all_tracts:
#     if current == j:
#       # third column - count of unique tract across all regions
#       tracts_in_regions[i][2] += 1

# header = "ID, Cluster, Count"
# v = open('C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\code\\test.csv', 'w')
# np.savetxt(v, tracts_in_regions, fmt='%i', delimiter=',', header=header, comments = '')

# r = csv.reader(v)
# row0 = r.next()
# row0.append('berry')

# print(set_all_tracts)

# f = open("heatmap_symbology_new.txt", "a")
# f.seek(0)                        # <- This is the missing piece
# f.truncate()
# np.savetxt(f, tracts_in_regions, fmt='%i')
# f.close()

# ** end individual symbology
#---------------------------------------------------#

# **begin all tracts symbology

# i'm only checking a specific cluster
# reminder to look for region-1 in flatclusters because the regions dont have a 0-indexed column in the csv file
# this will hold every region marked as cluster "test"
with open("./summer2024/util/heatmap_flatclusters_{num}.txt".format(num = num_flatclusters), 'r') as file:
  flatclusters = np.loadtxt(file)

cois = open('./summer2024/output/iowa_cois_{num}.csv'.format(num = num_flatclusters), 'w+')
writer = csv.writer(cois)
header = ['ID']
for c in (set(flatclusters[:,1])):
  header.append("Cluster " + str(int(c)))
# data.close()

A = np.zeros([size, len(set(flatclusters[:,1])) + 1], dtype=np.int16)
for i in range(size):
  A[i][0] = i

# print(A)

def all_counts(test=int):
  # i'm only checking a specific cluster
  # reminder to look for region-1 in flatclusters because the regions dont have a 0-indexed column in the csv file
  test = int(test)

  # this will hold every region marked as cluster "test"
  regions = []

  # generate the list of regions in cluster "test"
  for row in flatclusters:
    if row[1] == test:
      regions.append(int(row[0]))

  # this will hold all of the tracts from all regions in "test"
  all_tracts = []

  # clusters[region][2] is the list of tracts in a given number
  for region in regions:
    for tracts in clusters[region][2].split():
      all_tracts.append(tracts)

  # get a list of unique tracts 
  set_all_tracts = list(set(all_tracts))

  # this is the np array that will become the file
  # tracts_in_regions = np.zeros([len(set_all_tracts), 3], dtype=np.int16)

  # for each unique tract
  for i in range(len(set_all_tracts)):
    current = set_all_tracts[i]

    # first column - given a GEOID, what is the tract id? geoids holds the mapping from geoid to ID
    # data[i][0] = geoids.get(current)
    # second column is simply the cluster number, "test"
    # tracts_in_regions[i][1] = test

    # go through list of all census tracts and count how many times a unique tract appears
    for j in all_tracts:
      if current == j:
        # third column - count of unique tract across all regions
        A[geoids.get(j)][test] += 1

for c in set(flatclusters[:,1]):
  all_counts(c)

np.savetxt(cois, A, comments='', fmt='%i', delimiter=',', header=','.join(header))
cois.close()

#---------------------------------------------------------------#
# join the generated csv file with your tract shapefile
# then you can isolate the features by cluster number and apply a graduated symbology to get a heat map
#---------------------------------------------------------------#



# f = open("heatmap_symbology_alltracts.txt", 'a')
# f.seek(0)                        # <- This is the missing piece
# f.truncate()
# np.savetxt(f, data, fmt='%i')
# f.close()
# ** end all tracts symbology


#---------------------------old mhd notes------------------------------------#
# fig = plt.figure(figsize=(25, 10))
# dn = dendrogram(Z)
# plt.show()

# nodes: census tracts, always
# regions: what we have, until now, been calling clusters:
    # school districts
    # municipalities
    # clusters from summary statistics
# clusters: now we are talking about the clusters being formed using the mhd measure. 
    # These will ultimately be called "communities". 
    # They will be sets of census tracts that have been identified as being part of the same community
# heatmap: once we have the community clusters identified, we will create a heatmap for each community. 
    # Each census tract within the community will have an int assigned to it, which is the count of the number of regions it is in. 
    # That will give us a sense of how many regions overlapped in what areas of the community that were used to define the community.

# def tract_to_tract (a, b):
#     return tract_dists[a, b]

# def tract_to_cluster(a, B):
#     min = np.inf
#     for b in B:
#         dist = tract_dists[a, b]
#         if dist < min:
#             min = dist
#     return min

# # is this ever 0?
# def cluster_to_cluster(A, B):
#     sum = 0
#     for a in A:
#         sum += tract_to_cluster(a, B)
#     return 1/np.abs(sum)

# def mhd_clusters(A, B):
#     return max(cluster_to_cluster(A, B), cluster_to_cluster(B, A))

# def cluster_to_community(A, bB):
#     min = np.inf
#     for B in bB:
#         dist = mhd_clusters(A, B)
#         if dist < min:
#             min = dist
#     return min

# def community_to_community(aA, bB):
#     sum = 0
#     for A in aA:
#         sum += cluster_to_community(A, bB)
#     return 1/np.abs(sum)

# def mhd_communities(aA, bB):
#     return max(community_to_community(aA, bB), community_to_community(bB, aA))

# r1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# r2 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# print(cluster_to_cluster(r1, r2))
# print(cluster_to_cluster(r2, r1))
# print(mhd_clusters(r1, r2))
# ---------------------------------------------------------------#
