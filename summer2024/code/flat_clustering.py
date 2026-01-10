import numpy as np
import json
import scipy
import matplotlib.pyplot as plt
import statistics
from scipy.cluster.hierarchy import fclusterdata, linkage
import pickle

# a custom function that just computes Euclidean distance
# p1, p2 are 1D vectors specifying a pair of points
def mydist(p1, p2, G=pickle.load(open('tract_graph.pickle', 'rb'))):
    # print(p1, p2)

    # only cluster if p1 and p2 represent adjacent points
    # what about null values? unsure if they exist in data
    if(G.has_edge(p1[0], p2[0])):
        diff = np.abs(p1[1] - p2[1])
    else:
        diff = 5e7
    # return np.vdot(diff, diff) ** 0.5
    return diff

# suppress scientific notation for console output
np.set_printoptions(suppress=True)

# json file with tract polygons and census data
with open('C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\shapefiles\\tl_2022_19_tract_ss_2.json', 'r') as dict:
    tract_json = json.load(dict)

# N x N matrix holding distances between tracts
# run distances.py first to get mat
tract_dists = np.loadtxt("C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\tract_dists.txt")

# how many tracts are there
size = len(tract_json["tracts"])

#-----------------------begin main code----------------------------#
# this code only runs if test.py is run
if __name__ == "__main__":        


    # choose the given statistic you want to analyze
    # use histograms.py to determine the distribution type
    stat = "DP03_0038P"

    # create an N x 2 matrix where A[n, 0] is the tract number and A[n, 1] is the value for the given statistic   
    # maybe doesnt need to be float64
    A = np.zeros([size, 2], dtype=np.float64)
    for i in range(size):
        newrow = [i, tract_json["tracts"][i][stat]]
        A[i] = newrow
    print(A)

    #-----------------------old; basically this shows you what got clustered at each step----------------------------#
    # default = euclidian distance
    # condensed_dist_matrix = scipy.spatial.distance.squareform(A)
    # read python docs
    # Z = linkage(A, metric=mydist)

    # f = open("linkage.txt", "a")
    # f.seek(0)                        # <- This is the missing piece
    # f.truncate()

    # # output = "C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\linkage.txt"
    # np.savetxt("linkage.txt", Z, fmt = '%i')
    # f.close()

    # k = 0
    # cluster_steps = {}

    # for i in range(size):
    #     cluster_steps[i] = {i}

    # k = 0
    # for row in Z:
    #     # thisdict[k] = {Z[k,0], Z[k, 1]}
    #     cluster_steps.update({size + k: cluster_steps.get(Z[k, 0]).union(cluster_steps.get(Z[k, 1]))})
    #     k = k + 1

    # f = open("dict.txt", "a")
    # f.seek(0)                        # <- This is the missing piece
    # f.truncate()

    # for key, value in cluster_steps.items():
    #     if(key > 895):
    #         f.write(f"{key}: {value}" + "\n")
    # f.close()
    #-----------------------end of old stuff and cluster steps----------------------------#

    # grab just the statistic values
    col = A[:, 1]

    median = statistics.median(col)
    mean = statistics.mean(col)
    print("Mean: " + str(mean))
    print("0.1 Mean: " + str(mean * 0.1))
    print("0.15 Mean: " + str(mean * 0.15))
    print("0.2 Mean: " + str(mean * 0.2))
    print("Median: " + str(median))


    # threshold for fcluster

    # if the statistic is a percentage
    if(stat[len(stat) - 1] == "P"):
        t = mean * 0.15
        # t = mean
    # if the statistic is an estimate
    else:
        t = round(mean * 0.15)

    print("T: " + str(t))
    # currently 15%

    # find the SD and z score for each statistic
    sd = A.copy()
    sd[:, 1] = scipy.stats.zscore(col, 0, 0)
    print("SD: " + str(np.std(col)))

    # col2 = sd[:, 1]
    # print(col2)
    print(sd)

#-----------------------begin steps for gaussian distribution----------------------------#
    # begin gaussian
    f = open("sd.txt", "a")
    f.seek(0)                        # <- This is the missing piece
    f.truncate()

    np.savetxt("sd.txt", sd[:,1], fmt = '%i')
    f.close()

    flat = fclusterdata(sd, 0.5, criterion='distance', metric=mydist)
    print(flat)
#-----------------------end steps for gaussian distribution----------------------------#

#-----------------------begin steps for power law distribution----------------------------#
    # C = A.copy()
    # col2 = C[:, 1]

    # p = np.percentile(col, 85)
    # print("85th percentile:" + str(p))

    # for i in range(len(col2)):
    #     if(col2[i] >= p):
    #         col2[i] = 1
    #     else:
    #         col2[i] = 0

    # flat = fclusterdata(C, 0.5, criterion='distance', metric=mydist)
    # print(flat)
#-----------------------end steps for power law distribution----------------------------#

    # save flat clusters
    C = np.zeros([size, 2], dtype=np.float64)
    for i in range(size):
        newrow = [i, flat[i]]
        C[i] = newrow

    f = open("flatclusters.txt", "a")
    f.seek(0)                        # <- This is the missing piece
    f.truncate()

    # this is the underlying piece for GIS maps - will change for each statistic
    # IMPORTANT: save a copy of GIS maps or they will be overwritten by next run 
    # 1. import flatclusters.txt to GIS software
    # 2. join flatclusters.txt with shapefile
    # 3. color map by Field2 (indicates flat cluster number)
    np.savetxt("flatclusters.txt", C, fmt = '%i')
    f.close()

    plt.hist(col, bins='auto')
    plt.show()
    #-----------------------end main code----------------------------#

