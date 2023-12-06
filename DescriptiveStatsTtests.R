# Load packages
library(readr)
library(dplyr)

#########################
## Load data

# Base directory
base_dir <- "L:/LovbeskyttetMapper01/StenoSleepQCGM/Concatenated data"

# Load the nightly data
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_all_11.csv'), col_types = cols())

# Remove NaN
complete_dataset <- na.omit(complete_dataset)

##########################
## TST

# Extract columns of interest
TST <- complete_dataset %>% select(TST)

# Recommended sleep duration
recommended1 <- 8*60
recommended2 <- 9*60

# Conducting the one-sample t-test
t_test_result1 <- t.test(x = TST, mu = recommended1, alternative = "two.sided", 
                        conf.level = 0.95)
t_test_result2 <- t.test(x = TST, mu = recommended2, alternative = "two.sided", 
                         conf.level = 0.95)

# Displaying the t-test results
cat("Results for t-test comparing TST with 8 hours:\n")
print(t_test_result1)
cat("Results for t-test comparing TST with 9 hours:\n")
print(t_test_result2)

#hist(TST$TST)
#qqnorm(TST$TST, pch = 1, frame = FALSE)
#qqline(TST$TST, col = "steelblue", lwd = 2)

##########################
## TIR

# Extract columns of interest
TIR <- complete_dataset %>% select(TIR)

# Recommended
recommended <- 70

# Conducting the one-sample t-test
t_test_result <- t.test(x = TIR, mu = recommended, alternative = "two.sided", 
                         conf.level = 0.95)

# Displaying the t-test results
cat("Results for t-test comparing TIR with 70%:\n")
print(t_test_result)

###########################
## TAR

# Extract columns of interest
TAR <- complete_dataset %>% select(TAR)

# Recommended
recommended <- 25

# Conducting the one-sample t-test
t_test_result <- t.test(x = TAR, mu = recommended, alternative = "two.sided", 
                        conf.level = 0.95)

# Displaying the t-test results
cat("Results for t-test comparing TAR with 25%:\n")
print(t_test_result)

############################
## TBR

# Extract columns of interest
TBR <- complete_dataset %>% select(TBR)

# Recommended
recommended <- 4

# Conducting the one-sample t-test
t_test_result <- t.test(x = TBR, mu = recommended, alternative = "two.sided", 
                        conf.level = 0.95)

# Displaying the t-test results
cat("Results for t-test comparing TBR with 4%:\n")
print(t_test_result)


###############################
## WASO

# Extract columns of interest
WASO <- complete_dataset %>% select(WASO)

# Recommended
recommended <- 40

# Conducting the one-sample t-test
t_test_result <- t.test(x = WASO, mu = recommended, alternative = "two.sided", 
                        conf.level = 0.95)

# Displaying the t-test results
cat("Results for t-test comparing WASO with 40 min:\n")
print(t_test_result)

##################################
## SOL

# Extract columns of interest
SOL <- complete_dataset %>% select(Latency)

# Recommended
recommended <- 30

# Conducting the one-sample t-test
t_test_result <- t.test(x = SOL, mu = recommended, alternative = "two.sided", 
                        conf.level = 0.95)

# Displaying the t-test results
cat("Results for t-test comparing SOL with 30 min:\n")
print(t_test_result)

####################################
## Efficiency

# Extract columns of interest
Efficiency <- complete_dataset %>% select(Efficiency)

# Recommended
recommended <- 85

# Conducting the one-sample t-test
t_test_result <- t.test(x = Efficiency, mu = recommended, alternative = "two.sided", 
                        conf.level = 0.95)

# Displaying the t-test results
cat("Results for t-test comparing Efficiency with 85%:\n")
print(t_test_result)

#####################################
## CV

# Extract columns of interest
CV <- complete_dataset %>% select(cv)

# Recommended
recommended <- 0.36

# Conducting the one-sample t-test
t_test_result <- t.test(x = CV, mu = recommended, alternative = "two.sided", 
                        conf.level = 0.95)

# Displaying the t-test results
cat("Results for t-test comparing CV with 36%:\n")
print(t_test_result)

###################################

# Mean of TST for each individual
mean_TST_per_individual <- complete_dataset %>%
  group_by(id) %>%
  summarize(mean_TST = mean(TST))

# Output the mean TST for each individual
print(mean_TST_per_individual, n=23)



