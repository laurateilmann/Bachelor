# Load libraries
library(dplyr)
library(readr)
library(zoo)
library(lme4)
library(stats)
library(olsrr)

# Set your base directory
base_dir <- "L:/LovbeskyttetMapper01/StenoSleepQCGM/Concatenated data"

# Load nightly data
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_all_11.csv'), col_types = cols())
complete_dataset <- complete_dataset %>% rename(`SleepQ` = `Sleep quality`)

# Handling missing and infinite values
complete_dataset <- na.omit(complete_dataset)


################################
## WASO vs. CV - Nightly

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

# Residuals
residuals <- y_est - y

# Plot histogram of residuals
library(ggplot2)
ggplot(residuals, aes(x = WASO)) +
  geom_histogram(fill = "skyblue", color = "black", bins = 20) +
  ggtitle("Histogram of WASO nightly Residuals") +
  xlab("Residual Value") +
  ylab("Frequency")

# Save residuals to a CSV file
output_folder <- file.path(base_dir, "Residuals")
residuals_file <- file.path(output_folder, "residuals_Model_WN.csv")

write.csv(residuals, file = residuals_file, row.names = FALSE)

# Visualization of the model
# # Calculate predictions and standard errors manually
# new_data <- data.frame(cv = seq(min(standardized_data$cv), max(standardized_data$cv), length.out = 100))  # Create a sequence of values for CV
# 
# # Predictions
# preds <- predict(model, newdata = new_data, re.form = NA, allow.new.levels = TRUE)
# 
# # Extract fixed effects standard errors
# pred_se <- sqrt(diag(vcov(model)))
# 
# # Combine predictions and standard errors into a data frame
# pred_data <- cbind(new_data, preds, pred_se)
# colnames(pred_data)[2:3] <- c("predicted", "std.error")
# 
# # Calculate upper and lower bounds for uncertainty intervals
# pred_data <- transform(pred_data, 
#                        upper = predicted + std.error,
#                        lower = predicted - std.error)
# 
# # Plotting predictions and uncertainty intervals
# library(ggplot2)
# 
# ggplot(pred_data, aes(x = cv, y = predicted)) +
#   geom_line() +
#   geom_ribbon(aes(ymin = lower, ymax = upper), fill = "lightgrey", alpha = 0.5) +
#   geom_point(data = standardized_data, aes(x = cv, y = WASO, color = as.factor(id))) +
#   labs(x = "CV", y = "WASO", title = "WASO against CV") +
#   theme_minimal()

#######################################

## Efficiency vs. CV 

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

# Residuals
residuals <- y_est - y

# Plot histogram of residuals
library(ggplot2)
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
## WASO vs. CV - Hourly

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

# Residuals
residuals <- y_est - y

# Plot histogram of residuals
library(ggplot2)
ggplot(residuals, aes(x = WASO)) +
  geom_histogram(fill = "skyblue", color = "black", bins = 20) +
  ggtitle("Histogram of WASO hourly Residuals") +
  xlab("Residual Value") +
  ylab("Frequency")

# Save residuals to a CSV file
output_folder <- file.path(base_dir, "Residuals")
residuals_file <- file.path(output_folder, "residuals_Model_WH.csv")

write.csv(residuals, file = residuals_file, row.names = FALSE)