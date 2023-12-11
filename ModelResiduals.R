###############################################################################
# Authors: MGRO0154 & LTEI0004

# Compute the residuals of the three derived models and export as CSV.
###############################################################################

# Load libraries
library(dplyr)
library(readr)
library(lme4)
library(ggplot2)

# Set your base directory
base_dir <- "L:/LovbeskyttetMapper01/StenoSleepQCGM/Concatenated data"

# Load nightly data
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_all_11.csv'), col_types = cols())
complete_dataset <- complete_dataset %>% rename(`SleepQ` = `Sleep quality`)

# Handling missing and infinite values
complete_dataset <- na.omit(complete_dataset)


################################
## Model_WN

# Define the independent and dependent variables
x <- complete_dataset %>% select(3:12)
y <- complete_dataset %>% select(WASO)

# Standardize data
x_stan <- scale(x, center = TRUE, scale = TRUE)

# Extract ID
Id <- complete_dataset %>% select(id)

# Create a new data frame combining x_stan and y_stan
standardized_data <- data.frame(x_stan, y, id=Id)

# Model
model <- lmer("WASO ~ cv + (1 | id)", data = standardized_data)

# Predictions
y_est <- predict(model, standardized_data)

# Plot y against y_est
y_plot <- data.frame(y = y, y_est = y_est)
min_val <- min(min(y), min(y_est))
max_val <- max(max(y), max(y_est))
# Creating a plot with equal axes
plot(y_plot, xlim = c(min_val, max_val), ylim = c(min_val, max_val),
     xlab = "y", ylab = "y_est", main = "Scatterplot of y and y_est")
abline(a = 0, b = 1, col = "red")

# Residuals
residuals <- y_est - y

# Plot histogram of residuals
ggplot(residuals, aes(x = WASO)) +
  geom_histogram(fill = "skyblue", color = "black", bins = 20) +
  ggtitle("Histogram of WASO nightly Residuals") +
  xlab("Residual Value") +
  ylab("Frequency")

# Save residuals to a CSV file
output_folder <- file.path(base_dir, "Residuals")
residuals_file <- file.path(output_folder, "residuals_Model_WN.csv")
write.csv(residuals, file = residuals_file, row.names = FALSE)

#######################################
## Model_SE

# Define the independent and dependent variables
x <- complete_dataset %>% select(3:12)
y <- complete_dataset %>% select(Efficiency)

# Standardize data
x_stan <- scale(x, center = TRUE, scale = TRUE)

# Extract ID
Id <- complete_dataset %>% select(id)

# Create a new data frame combining x_stan and y_stan
standardized_data <- data.frame(x_stan, y, id=Id)

# Model
model <- lmer("Efficiency ~ min + max + (1 | id)", data = standardized_data)

# Predictions
y_est <- predict(model, standardized_data)

# Plot y against y_est
y_plot <- data.frame(y = y, y_est = y_est)
min_val <- min(min(y), min(y_est))
max_val <- max(max(y), max(y_est))
# Creating a plot with equal axes
plot(y_plot, xlim = c(min_val, max_val), ylim = c(min_val, max_val),
     xlab = "y", ylab = "y_est", main = "Scatterplot of y and y_est")
abline(a = 0, b = 1, col = "red")

# Residuals
residuals <- y_est - y

# Plot histogram of residuals
ggplot(residuals, aes(x = Efficiency)) +
  geom_histogram(fill = "skyblue", color = "black", bins = 20) +
  ggtitle("Histogram of Efficiency Residuals") +
  xlab("Residual Value") +
  ylab("Frequency")

# Save residuals to a CSV file
output_folder <- file.path(base_dir, "Residuals")
residuals_file <- file.path(output_folder, "residuals_Model_SE.csv")
write.csv(residuals, file = residuals_file, row.names = FALSE)

################################
## Model_WH

# Load hourly data
complete_dataset_h <- read_csv(file.path(base_dir, 'concatenated_hourly_all_11.csv'), col_types = cols())

# Handling missing and infinite values
complete_dataset_h <- na.omit(complete_dataset_h)

# Define the independent and dependent variables
x <- complete_dataset_h %>% select(3:12)
y <- complete_dataset_h %>% select(WASO)

# Standardize data
x_stan <- scale(x, center = TRUE, scale = TRUE)

# Extract ID
Id <- complete_dataset_h %>% select(id)

# Create a new data frame combining x_stan and y_stan
standardized_data <- data.frame(x_stan, y, id=Id)

# Model
model <- lmer("WASO ~ cv + (1 | id)", data = standardized_data)

# Predictions
y_est <- predict(model, standardized_data)

# Plot y against y_est
y_plot <- data.frame(y = y, y_est = y_est)
min_val <- min(min(y), min(y_est))
max_val <- max(max(y), max(y_est))
# Creating a plot with equal axes
plot(y_plot, xlim = c(min_val, max_val), ylim = c(min_val, max_val),
     xlab = "y", ylab = "y_est", main = "Scatterplot of y and y_est")
abline(a = 0, b = 1, col = "red")

# Residuals
residuals <- y_est - y

# Plot histogram of residuals
ggplot(residuals, aes(x = WASO)) +
  geom_histogram(fill = "skyblue", color = "black", bins = 20) +
  ggtitle("Histogram of WASO hourly Residuals") +
  xlab("Residual Value") +
  ylab("Frequency")

# Save residuals to a CSV file
output_folder <- file.path(base_dir, "Residuals")
residuals_file <- file.path(output_folder, "residuals_Model_WH.csv")
write.csv(residuals, file = residuals_file, row.names = FALSE)
