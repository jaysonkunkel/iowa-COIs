import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json
import scipy
from scipy.cluster.hierarchy import fcluster


# suppress scientific notation
np.set_printoptions(suppress=True)

# this is step 3
# step 4 is mhd.py

input = "./summer2024/util/tract_dists.txt"
tract_dists = np.loadtxt(input)

with open('./summer2024/util/geoid_index.json', 'r') as file:
  geoids = json.load(file)

with open('./summer2024/util/clusters_tracts.csv', 'r') as file:
  csv_reader = csv.reader(file)
  clusters = list(csv_reader)

#-----------------------mhd definitions----------------------------#
# distance between two census tracts
def tract_to_tract (a, b):
    return tract_dists[a, b]

# distance between a tract and a region
def tract_to_cluster(a, B):
    min = np.inf
    for b in B:
        b = geoids.get(b)
        dist = tract_dists[a, b]
        if dist < min:
            min = dist
    return min

# difference between two regions
def cluster_to_cluster(A, B):
    sum = 0
    for a in A:
        # get index from geoid
        a = geoids.get(a)
        sum += tract_to_cluster(a, B)
    return sum / len(A)
    # return 0 if sum == 0 else 1/np.abs(sum)

def mhd_clusters(A, B):
    return max(cluster_to_cluster(A, B), cluster_to_cluster(B, A))

# wrapper function to generate list of tracts to represent a region
def heatmap(A, B):
  tracts1 = clusters[int(A[0])][2].split()
  tracts2 = clusters[int(B[0])][2].split()
  # print(tracts1)
  # print(tracts2)
  return mhd_clusters(tracts1, tracts2)
#---------------------------------------------------#

#-----------------------start of linkage----------------------------#
## I needed two columns of indices because the linkage function kept getting mad
# afaik it only needs the first column because I'm using that to index
# len clusters is the number of regions we found
huh = np.zeros([len(clusters), 2], dtype=np.int16)
for i in range(len(clusters)):
  newrow = [i, i]
  huh[i] = newrow

# can maybe skip this step?
Z = scipy.cluster.hierarchy.linkage(huh, method='complete', metric=heatmap)

output = './summer2024/util/heatmap_linkage.txt'

f = open(output, "a")
f.seek(0)                        # <- This is the missing piece
f.truncate()

np.savetxt(output, Z, fmt = '%i')
f.close()
#-----------------------end of linkage----------------------------#


# print(Z)

#-----------------------start of flatclustering----------------------------#
# load the linkage array
Z = np.loadtxt("./summer2024/util/heatmap_linkage.txt")

# t = max clusters
# 327 (number of school districts) generated 205 clusters
# 50 generated 44 flat clusters
t = round(50)

# generate flat clusters
flat = fcluster(Z, t, criterion='maxclust')

# C is the flatclusters + an index column
C = np.zeros([len(clusters), 2], dtype=np.int16)
for i in range(len(clusters)):
    newrow = [i, flat[i]]
    C[i] = newrow

f = open("./summer2024/util/heatmap_flatclusters.txt", "a")
f.seek(0)                        # <- This is the missing piece
f.truncate()
np.savetxt(f, C, fmt='%i')
f.close()

# how many flatclusters we end up with
print(len(set(C[:,1])))
#-----------------------end of flatclustering----------------------------#



  



#  ** map tract id to geoid for lookup because im stupid

# dict = test.dict.copy()
# size = len(dict["tracts"])
# indexes = {}

# for i in range(size):
#   indexes.update({dict['tracts'][i]['GEOID']: i})

# with open('geoid_index.json', 'w') as result:
#     json.dump(indexes, result)