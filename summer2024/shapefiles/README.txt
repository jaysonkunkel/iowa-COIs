Census boundary shapefiles:

	tl_2022_19_tract: unmodified census tract shapefile

	tl_2023_19_bg: unmodified block group shapefile

	tl_2022_19_tabblock20: unmodified census block shapefile

		https://catalog.data.gov/organization/census-gov
		note that there are field discrepancies between shapefiles

	tl_2022_19_tract_neighbors: census tract shapefile with list of neighbors and nested block groups, but no ID field

	tl_2022_19_tract_neighbors_ss: most recent shapefile with neighbors and groups and summary statistics, also an ID field for indexing

	tl_2022_19_tract_neighbors_ss.json: JSON representation of shapefile
		https://mapshaper.org
		note that this file has a redundant "tracts" category. I think this is an artifact of me trying to have the tract data AND an adjacency list so whenever you see [tracts] in the code that's what it means

	IA_counties: county shapefile with MGGG-processed data

Other shapefiles:

	Electrical_Service_Boundaries: shapefile for IA electrical provider boundaries

	Electrical_Service_Boundaries_Cleaned: same but with rural districts removed

	IA_municipalities: shapefile of city/town boundaries in IA
	
	IA_School_Districts_2023-2024: what it says
	

