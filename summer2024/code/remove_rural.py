import numpy as np
import csv
import json

# this is step 1
# step 2 is overlap.py

def find_overlap(statistic, rural_clusters):
  # for each flat cluster
  for cluster_num in clusters:

    # ignore giant rural cluster(s)
    if cluster_num in rural_clusters:
      continue

    newrow = [statistic]
    # keep track of the tracts in a given cluster
    clusters_in_tract = []
    newrow.append(cluster_num)

    # for each census tract
    for tract in range(len(tracts)):
      # if tract is in this cluster
      if (flat[tract,1] == cluster_num): 
        # add it to the list
        clusters_in_tract.append(int(tract_json['tracts'][tract]['GEOID']))
    
    # add information
    newrow.append(clusters_in_tract)
    data.append(newrow)

#-----------------------begin main code----------------------------#
output_path = './summer2024/util/clusters_tracts.csv'

# file to store information
with open(output_path, 'r') as file:
    csv_reader = csv.reader(file)
    data = list(csv_reader)

#-----------------------manual input - will change each run---------#
# which statistic to use
statistic = "DP04_0134E"

# indicates the giant "rural" cluster(s)
# find the corresponding cluster number in flatclusters.txt or in GIS
rural_clusters = [46]
#-----------------------end manual input----------------------------#

# with open('c:\\Users\\jayso\\OneDrive\\Documents\\tracts_to_blocks.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     blocks = list(csv_reader)

# flat clusters
input_path = open('flatclusters.txt')
flat = np.loadtxt(input_path).copy()
input_path.close()

# first column - indices of census tracts
tracts = flat[:,0]

# second column - the cluster a tract is in
clusters = map(int, set(flat[:,1]))

# json file with tract polygons and census data
with open('./summer2024/util/tl_2022_19_tract_ss_2.json', 'r') as dict:
    tract_json = json.load(dict)

find_overlap(statistic, rural_clusters)
#-----------------------end main code----------------------------#

# Writing to CSV file
with open(output_path, 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerows(data)


