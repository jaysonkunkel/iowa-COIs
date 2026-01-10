library(foreign)
library(dplyr)

# read in geography data
tract <- read.dbf("C:\\Users\\jayso\\Downloads\\tl_2022_19_tract\\tl_2022_19_tract.dbf", as.is = F)
bg <- read.dbf("C:\\Users\\jayso\\Downloads\\tl_2023_19_bg\\tl_2023_19_bg.dbf", as.is = F)
block <- read.dbf("C:\\Users\\jayso\\Downloads\\tl_2022_19_tabblock20\\tl_2022_19_tabblock20.dbf", as.is = F)

# copies of geography data
tractcopy <- tract
bgcopy <- bg
blockcopy <- block

# add new columns to hold nested sub-geographies
tractcopy <- tractcopy %>% mutate(groups = "")
tractcopy <- tractcopy %>% mutate(blocks = "")
bgcopy <- bgcopy %>% mutate(blocks = "")

# which tract is each sub-geography in (basically just removes the "19")
bgcopy <- bgcopy %>% mutate(unique_tract = substring(bgcopy$GEOID, 3, 11))
tractcopy <- tractcopy %>% mutate(unique_tract = substring(tractcopy$GEOID, 3))
blockcopy <- blockcopy %>% mutate(unique_tract = substring(blockcopy$GEOID20, 3, 11))

# which block group is each sub-geography in
blockcopy <- blockcopy %>% mutate(unique_bg = substring(blockcopy$GEOID20, 3, 12))
bgcopy <- bgcopy %>% mutate(unique_bg = substring(bgcopy$GEOID, 3))

# the three sections below are the important ones
# these take a LONG time to run

# generate list of block groups for each tract

# for each block group
for(i in 1:length(bgcopy$unique_tract)){
  # for each tract
  for(j in 1:length(tractcopy$unique_tract)){
    # check if bg county and tract matches census tract
    # some tract nums. are repeated in multiple counties
    if(bgcopy$unique_tract[i] == tractcopy$unique_tract[j]) {
      tractcopy$groups[j] <- paste(tractcopy$groups[j], bgcopy$GEOID[i])
      break
    } 
  }
}


# generate list of blocks for each block group

# for each block
for(i in 1:length(blockcopy$unique_bg)){
  # for each block group
  for(j in 1:length(bgcopy$unique_bg)){
    # check if block is in block group
    if(blockcopy$unique_bg[i] == bgcopy$unique_bg[j]) {
      bgcopy$blocks[j] <- paste(bgcopy$blocks[j], blockcopy$GEOID20[i])
      break
    } 
  }
}


# generate list of blocks for each tract

# for each block group
for(i in 1:length(bgcopy$unique_tract)){
  # for each tract
  for(j in 1:length(tractcopy$unique_tract)){
    # check if block group in tract and add list of blocks
    if(bgcopy$unique_tract[i] == tractcopy$unique_tract[j]) {
      tractcopy$blocks[j] <- paste(tractcopy$blocks[j], bgcopy$blocks[i])
      break
    } 
  }
}

# replace whitespace with commas and trim the last one
# tractcopy2$groups <- gsub(" ", ", ", tractcopy2$groups)
# tractcopy2$groups <- trimws(tractcopy2$groups, whitespace = ", ")

# same thing as above
# neighbors <- read.dbf("C:\\Users\\jayso\\OneDrive\\Desktop\\MAP\\neighbors\\tl_2022_19_tract_neighbors.dbf", as.is = F)
# neighbors$groups <- gsub(" ", ", ", neighbors$groups)
# neighbors$groups <- trimws(neighbors$groups, whitespace = ", ")

# I don't remember why I did this tbh
# neighbors <- neighbors %>% mutate(GEOID_FULL = paste("1400000US", sep = "", GEOID))

# me trying to force data to be numeric instead of text
# dp02 <- read.csv("C:\\Users\\jayso\\OneDrive - Grinnell College\\gerrymandering\\dp02\\ACSDP5Y2022.DP02-DataSS.csv")
# dp03 <- read.csv("C:\\Users\\jayso\\OneDrive - Grinnell College\\gerrymandering\\dp03\\ACSDP5Y2022.DP03-DataSS.csv")
# dp04 <- read.csv("C:\\Users\\jayso\\OneDrive - Grinnell College\\gerrymandering\\dp04\\ACSDP5Y2022.DP04-DataSS.csv")
# dp05 <- read.csv("C:\\Users\\jayso\\OneDrive - Grinnell College\\gerrymandering\\dp05\\ACSDP5Y2022.DP05-DataSS.csv")

# dp02 <- data.frame(dp02[1:2], sapply(dp02[,3:ncol(dp02)], as.numeric))
# dp03 <- data.frame(dp03[1:2], sapply(dp03[,3:ncol(dp03)], as.numeric))
# dp04 <- data.frame(dp04[1:2], sapply(dp04[,3:ncol(dp04)], as.numeric))
# dp05 <- data.frame(dp05[1:2], sapply(dp05[,3:ncol(dp05)], as.numeric))

# write.csv(dp02, "dp02_new.csv")
# write.csv(dp03, "dp03_new.csv")
# write.csv(dp04, "dp04_new.csv")
# write.csv(dp05, "dp05_new.csv")

# dp04$DP04_0134E <- as.numeric(as.character(dp04$DP04_0134E))

# note that some file writing was done via console, look thru rhistory file for these
