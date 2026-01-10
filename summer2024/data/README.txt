american community survey (acs) 5-year estimates at the Iowa census tract level

dp02: social characteristics
https://data.census.gov/table?q=dp02&g=040XX00US19,19$1400000

dp03: economic characteristics
https://data.census.gov/table?q=dp03&g=040XX00US19,19$1400000

dp04: housing characteristics
https://data.census.gov/table?q=dp04&g=040XX00US19,19$1400000

dp05: demographic & housing estimates

I excluded some factors like some age cohorts in my summary statistics. so if you want a complete analysis you may have to make a new shapefile / json and add the desired statistics.

each folder contains: 
	original, unmodified csv file
	modified csv file with only summary statistics (i think this is the one joined with the shapefile)
	3 metadata files:
		original csv file
		excel worksheet of original (for color coding)
		excel worksheet of summary statistics

summary statistics were chosen from the DVRPC paper