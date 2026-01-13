import geopandas as gpd
import csv

import os
import sys

import flat_clustering

import matplotlib
import numpy as np
import networkx as nx
from networkx import Graph
import json
import scipy
from queue import Queue
import matplotlib.pyplot as plt
import math
import statistics
import csv
from collections import Counter

os.environ['GDAL_DATA'] = os.path.join(f'{os.sep}'.join(sys.executable.split(os.sep)[:-1]), 'Library', 'share', 'gdal')

# this is step 2
# step 1 is remove_rural.py

def find_overlap (source, target):

  # make the geometries match if necessary
  if source.crs != target.crs:
    source = source.to_crs(target.crs)
  source = source.reset_index(drop=True)

  # for each region in the input shapefile
  for index1, row1 in source.iterrows():
    polygon1 = row1['geometry']
    attributes1 = row1.drop('geometry')

    # make sure the polygon has positive area
    if polygon1.area == 0:
      continue 
    
    newrow = [statistic]
    clusters_intersect = []
    newrow.append(attributes1[source_attr])

    # for each region (tracts, blocks) in the other shapefile
    for index2, row2 in target.iterrows():
      polygon2 = row2['geometry']
      attributes2 = row2.drop('geometry')

      # make sure the polygon has positive area
      if polygon2.area == 0:
        continue

      # check if they intersect not just on the border
      # note: this may not work obsolete since polygon borders do not always line up across shapefiles
      if polygon1.intersects(polygon2) and not polygon1.touches(polygon2):
        clusters_intersect.append(int(attributes2[target_attr]))

    # add information
    newrow.append(clusters_intersect)
    data.append(newrow)

#-----------------------begin main code----------------------------#    
# source paths:
# electric_path = './summer2024/shapefiles/Electrical_Service_Boundaries_Cleaned/Electrical_Service_Boundaries_Cleaned.shp'
# school_path = './summer2024/shapefiles/Iowa_School_Districts_2023-2024/Iowa_School_Districts_2023-2024.shp'
# city_path = './summer2024/shapefiles/IA_municipalities/IA_municipalities.shp'

# target path:
# tract_path = './summer2024/shapefiles/tl_2022_19_tract_ss_2/tl_2022_19_tract_ss_2.shp'

# shapefile to read from
source_path = './summer2024/shapefiles/IA_municipalities/IA_municipalities.shp'

#shapefile we are overlapping with
target_path = './summer2024/shapefiles/tl_2022_19_tract_ss_2/tl_2022_19_tract_ss_2.shp'

# where we write information
output_path = './summer2024/util/clusters_tracts.csv'

# geodataframes to hold input
source_gdf = gpd.read_file(source_path)
target_gdf = gpd.read_file(target_path)

# change depending on which shapefile
statistic = "Municipality"

# indicates specific polygon in a statistic
source_attr = 'OBJECTID'

# indicates census tract
target_attr = 'GEOID'

with open(output_path, 'r') as file:
    csv_reader = csv.reader(file)
    data = list(csv_reader)

find_overlap(source_gdf, target_gdf)

# write information to file
with open(output_path, 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerows(data)
#-----------------------end main code----------------------------#

# when finished, make sure to clean up the csv file - remove brackets and commas

# ---------------------------------------------------------------#
# with open('c:\\Users\\jayso\\OneDrive\\Documents\\tracts_to_blocks.csv') as file:
#     csv_reader = csv.reader(file)
#     blocks = list(csv_reader)


# def overlap(source, target):
#   # source = source[source.is_valid]
#   # target = target[target.is_valid]

#   # source = source.explode()

#   if source.crs != target.crs:
#     source = source.to_crs(target.crs)
  
#   source = source.reset_index(drop=True)

#   # print(source.geometry.head())
#   # print(target.geometry.head())

#   for index1, row1 in source.iterrows():
#     polygon1 = row1['geometry']
#     attributes1 = row1.drop('geometry')
#     # print(f"   School district: {attributes1[source_attr]}\n")
#     for index2, row2 in target.iterrows():
#         polygon2 = row2['geometry']
#         attributes2 = row2.drop('geometry')
#         # print(type(polygon1), type(polygon2))
#         # print(f"{attributes1[source_attr]} {attributes2[target_attr]}\n" )
#         if not attributes1['Shape__Are'] == 0 and polygon1.intersects(polygon2) and not polygon1.touches(polygon2):
#           # print(f"   Intersects these tracts: {attributes2[target_attr]}\n")
#           newrow = [statistic, attributes1[source_attr], attributes2[target_attr], blocks[index2]]
#           data.append(newrow)
# ---------------------------------------------------------------#



