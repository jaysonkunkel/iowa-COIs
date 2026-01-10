import geopandas as gpd
import os
import sys

# credit: https://gis.stackexchange.com/questions/281652/finding-all-neighbors-using-geopandas

# this may or may not do something useful
os.environ['GDAL_DATA'] = os.path.join(f'{os.sep}'.join(sys.executable.split(os.sep)[:-1]), 'Library', 'share', 'gdal')

input = "C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\shapefiles\\tl_2022_19_tract_ss\\tl_2022_19_tract_ss.shp"
# input = "C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\shapefiles\\tl_2022_19_tabblock20\\tl_2022_19_tabblock20.shp"


# open file
gdf = gpd.read_file(input)

# add NEIGHBORS column
gdf["GID_NEIGHBORS"] = None  

# use 'GEOID' for tracts
# field names may change between geometries
for index, tract in gdf.iterrows():   

    # get 'not disjoint' countries
    neighbors = gdf[~gdf.geometry.disjoint(tract.geometry)].GEOID.tolist()

    # remove own name of the country from the list
    neighbors = [ name for name in neighbors if tract.GEOID != name ]

    # add names of neighbors as NEIGHBORS value
    gdf.at[index, "GID_NEIGHBORS"] = ", ".join(neighbors)
   
# save GeoDataFrame as a new file
output = "C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\shapefiles\\tl_2022_19_tract_ss\\tl_2022_19_tract_ss.shp"
# output = "C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\shapefiles\\tl_2022_19_tabblock20\\tl_2022_19_tabblock20.shp"
gdf.to_file(output)