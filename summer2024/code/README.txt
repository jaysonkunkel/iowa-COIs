list_neighbors.py creates a list of neighbors for each polygon in a given shapefile

geo-mapping.r creates a list of nested geographies (like what block groups are inside a given tract, what blocks are inside a block group) 
and also the reverse (which block group is a block in, which tract is a block group in)

.Rdata contains some helpful temp files

.Rhistory has some console commands that I used to write to files (instead of lines of body code)

distances.py calculates the distances from each node to each other node

histograms.py shows you the distribution for a given statistic
  - distributions.txt contains this information

flatclustering_census.py performs the first round of clustering on census data

remove_rural.py removes large, state-wide rural clusters and finds the census tracts within clusters

overlap.py finds the census tracts within non-census boundaries

flatclustering_all performs the second round of clustering on all 'communities' using mhd
