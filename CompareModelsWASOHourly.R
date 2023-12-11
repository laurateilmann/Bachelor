###############################################################################
# Authors: MGRO0154 & LTEI0004

# Compare regression models for hourly WASO.
###############################################################################

# Clear work space
rm(list = ls())

# Load packages
library(caret)
library(dplyr)
library(readr)
library(lme4)

# Set your base directory
base_dir <- "L:/LovbeskyttetMapper01/StenoSleepQCGM/Concatenated data"

# Load the hourly data
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_hourly_all_11.csv'), col_types = cols())

# Handling missing and infinite values
complete_dataset <- na.omit(complete_dataset)

# Define the independent and dependent variables
x <- complete_dataset %>% select(2:11)
y <- complete_dataset %>% select(WASO)

# Dimensions of x
N <- nrow(x)
M <- ncol(x)

# Extract ID
Id <- complete_dataset %>% select(id)

# Standardize data
x_stan <- scale(x, center = TRUE, scale = TRUE)

# Create a new data frame combining x_stan and y_stan
X <- data.frame(x_stan, y, id=Id)


###########################################################

## K-fold cross-validation

# Set seed for reproducibility. 
#set.seed(7645)

# Number of times cross-validation is performed
J = 20
# Number of folds in K-fold cross-validation
K = 5

# Initialize lists
# The derived model vs. baseline model
p_values_model_bl <- vector("list", K)
estimates_model_bl <- vector("list", K)
CI_model_bl <- vector("list",K)
# The ID model vs. baseline model
p_values_model2_bl <- vector("list", K)
estimates_model2_bl <- vector("list", K)
CI_model2_bl <- vector("list",K)
# The derived model vs. ID model
p_values_model_model2 <- vector("list", K)
estimates_model_model2 <- vector("list", K)
CI_model_model2 <- vector("list",K)


# Outer loop - number of times cross-validation and t-test is performed
for (j in 1:J) {
  
  # Initialize
  y_true <- c()
  y_model <- c()
  y_model2 <- c()
  y_baseline <- c()
  
  # Create folds
  CV <- list()
  CV$which <- createFolds(1:N, k = K, list = F)
  
  # Inner loop - cross-validation
  for (k in 1:K) {
    
    # Extract training and test set
    X_train <- X[CV$which != k, ]
    X_test <- X[CV$which == k, ]
    
    # Train models
    model <- lmer("WASO ~ cv + (1 | id)", data = X_train)
    model2 <- lmer("WASO ~ (1 | id)", data = X_train)
    
    # Model predictions
    y_est_model <- predict(model, X_test)
    y_est_model2 <- predict(model2, X_test)
    
    # Baseline model predictions
    mean_value <- mean(X_test$WASO)
    y_est_baseline <- data.frame(y_est_baseline = rep(mean_value, nrow(X_test)))
    
    # The true output values
    y_test <- X_test[11]
    
    # Save results
    y_model <- c(y_model, list(y_est_model))
    y_model2 <- c(y_model2, list(y_est_model2))
    y_baseline <- c(y_baseline, y_est_baseline)
    y_true <- c(y_true, y_test)
    
  }
  
  # Convert lists to vectors
  y_model <- unlist(y_model)
  y_model2 <- unlist(y_model2)
  y_baseline <- unlist(y_baseline)
  y_true <- unlist(y_true)
  
  # Compute loss
  z_model <- abs(y_true - y_model)**2
  z_model2 <- abs(y_true - y_model2)**2
  z_baseline <- abs(y_true - y_baseline)**2
  # Compute difference in loss
  z_model_bl <- z_model - z_baseline
  z_model2_bl <- z_model2 - z_baseline
  z_model_model2 <- z_model - z_model2
  
  # Compute p-value and CI for the differences between models
  t_test_model_bl <- t.test(z_model_bl, alternative = "two.sided", alpha = 0.05)
  t_test_model2_bl <- t.test(z_model2_bl, alternative = "two.sided", alpha = 0.05)
  t_test_model_model2 <- t.test(z_model_model2, alternative = "two.sided", alpha = 0.05)
  
  # Save p-value and CI
  p_values_model_bl[[j]] <- t_test_model_bl$p.value
  estimates_model_bl[[j]] <- t_test_model_bl$estimate
  CI_model_bl[[j]] <- t_test_model_bl$conf.int
  p_values_model2_bl[[j]] <- t_test_model2_bl$p.value
  estimates_model2_bl[[j]] <- t_test_model2_bl$estimate
  CI_model2_bl[[j]] <- t_test_model2_bl$conf.int
  p_values_model_model2[[j]] <- t_test_model_model2$p.value
  estimates_model_model2[[j]] <- t_test_model_model2$estimate
  CI_model_model2[[j]] <- t_test_model_model2$conf.int
  
}

# Print result
cat("Model vs. baseline")
for (j in 1:J) {
  cat(
    "Iteration", j, 
    ", estimate:", estimates_model_bl[[j]],
    ", p-value:", p_values_model_bl[[j]], 
    ", CI: [", CI_model_bl[[j]][1], ",", CI_model_bl[[j]][2], "]", 
    "\n"
  )
}
cat("ID model vs. baseline")
for (j in 1:J) {
  cat(
    "Iteration", j, 
    ", estimate:", estimates_model2_bl[[j]],
    ", p-value:", p_values_model2_bl[[j]], 
    ", CI: [", CI_model2_bl[[j]][1], ",", CI_model2_bl[[j]][2], "]", 
    "\n"
  )
}

cat("Model vs. ID model")
for (j in 1:J) {
  cat(
    "Iteration", j, 
    ", estimate:", estimates_model_model2[[j]],
    ", p-value:", p_values_model_model2[[j]], 
    ", CI: [", CI_model_model2[[j]][1], ",", CI_model_model2[[j]][2], "]", 
    "\n"
  )
}


