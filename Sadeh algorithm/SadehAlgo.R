library(devtools)
library("actigraph.sleepr")

file_path <- "H:\\Data\\Actigraph data\\Mind_fam01_ung60sec.agd" 
agd_data <- read_agd(file_path)

agd_sadeh = agd_data %>% apply_sadeh()

plot_activity(agd_sadeh,axis1)
