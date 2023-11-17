
# Set your base directory
base_dir <- "L:/LovbeskyttetMapper01/StenoSleepQCGM/Concatenated data"

# Load the nightly data
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_all_11.csv'), col_types = cols())

# Remove NaN
complete_dataset <- na.omit(complete_dataset)

# Extract columns of interest
TST <- complete_dataset %>% select(16)

# Recommended sleep duration
recommended_duration1 <- 8*60
recommended_duration2 <- 9*60

# Conducting the one-sample t-test
t_test_result1 <- t.test(x = TST, mu = recommended_duration1, alternative = "two.sided", 
                        conf.level = 0.95)
t_test_result2 <- t.test(x = TST, mu = recommended_duration2, alternative = "two.sided", 
                         conf.level = 0.95)

# Displaying the t-test results
print(t_test_result1)
print(t_test_result2)
