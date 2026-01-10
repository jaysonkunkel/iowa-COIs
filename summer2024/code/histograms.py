import numpy as np
import matplotlib.pyplot as plt
import json

# json file with tract polygons and census data
with open('C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\shapefiles\\tl_2022_19_tract_ss_2.json', 'r') as dict:
    tract_json = json.load(dict)

# how many tracts are there
size = len(tract_json["tracts"])

# N x 2 array to hold tract number and value of given statistic
tracts = np.zeros([size, 2], dtype=np.float64)
values = tracts[:, 1]

# populate array with statistic values
stat = "DP03_0038P"
for i in range(size):
    newrow = [i, tract_json["tracts"][i][stat]]
    tracts[i] = newrow

# plot the histogram
plt.hist(values, bins='auto')
plt.xlabel(stat)
plt.show()

# I forgot why I used this - ask eric?
# something to do with the curve of DP02_0067P being backwards?
#-----------------------------#
# C = tracts.copy()
# col2 = C[:, 1]

# for i in range(len(col2)):
#     col2[i] = 100 - col2[i]

# p = np.percentile(col2, 15)
# print("15th percentile:" + str(p))

# hist = plt.hist(col2, bins='auto')
# plt.xlabel(stat)
# plt.show()
#-----------------------------#


# matplotlib.pyplot.loglog(C[:, 1])

