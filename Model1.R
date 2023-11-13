# Load libraries
library(dplyr)
library(readr)
library(zoo)
library(lme4)
library(stats)
library(olsrr)

# Set your base directory
base_dir <- "L:/LovbeskyttetMapper01/StenoSleepQCGM/Concatenated data"

# Variable names
var_names <- list("TIR", "TAR", "TBR", "min", "max", "mean", "median", "std", "cv", "delta.IG")

################################
## Nightly

# Load the nightly data
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_all_11.csv'), col_types = cols())
complete_dataset <- complete_dataset %>% rename(`SleepQ` = `Sleep quality`)

# Handling missing and infinite values
complete_dataset <- na.omit(complete_dataset)


# Define the independent and dependent variables
x <- complete_dataset %>% select(3:12)
y <- complete_dataset %>% select(WASO)

# Standardize data
x_stan <- scale(x, center = TRUE, scale = TRUE)

# Extract ID
Id <- complete_dataset %>% select(id)

# Create a new data frame combining x_stan and y_stan
standardized_data <- data.frame(x_stan, y, id=Id)

# Model 1
model <- lmer("WASO ~ cv + (1 | id)", data = standardized_data)

# Predictions
y_est <- predict(model, standardized_data)

# Residuals
residuals <- y_est - y

# Plot histogram of residuals
library(ggplot2)
ggplot(residuals, aes(x = WASO)) +
  geom_histogram(fill = "skyblue", color = "black", bins = 20) +
  ggtitle("Histogram of WASO Residuals") +
  xlab("Residual Value") +
  ylab("Frequency")

# Save residuals to a CSV file
output_folder <- file.path(base_dir, "Residuals")
residuals_file <- file.path(output_folder, "residuals.csv")

# Create the output folder if it doesn't exist
if (!dir.exists(output_folder)) {
  dir.create(output_folder)
}

write.csv(residuals, file = residuals_file, row.names = FALSE)


