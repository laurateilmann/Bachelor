
rm(list = ls()) # Clear work space

# Package for decision tree
library(rpart)

# Package for Cross-Validation
library(caret)

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

### Nightly

# Load the nightly data
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_all_11.csv'), col_types = cols())
complete_dataset <- complete_dataset %>% rename(`SleepQ` = `Sleep quality`)

# Handling missing and infinite values
complete_dataset <- na.omit(complete_dataset)

# Define the independent and dependent variables
x <- complete_dataset %>% select(3:12)
y <- complete_dataset %>% select(Efficiency)

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
set.seed(7645)

# Number of times cross-validation is performed
J = 1
# Number of folds in K-fold cross-validation
K = 5

# Initialize
p_values_list <- vector("list", K)
estimates_list <- vector("list", K)
CI_list <- vector("list",K)


# Outer loop - number of times cross-validation and t-test is performed
for (j in 1:J) {
  
  # Initialize
  y_true <- c()
  y_model <- c()
  y_baseline <- c()
  
  # Create folds
  CV <- list()
  CV$which <- createFolds(1:N, k = K, list = F)
  
  # Inner loop - cross-validation
  for (k in 1:K) {
  
    # Extract training and test set
    X_train <- X[CV$which != k, ]
    X_test <- X[CV$which == k, ]
    
    # Train model
    model <- lmer("Efficiency ~ min + max + (1 | id)", data = X_train)
    #model <- lm("WASO ~ cv ", data = X_train)

    # Model predictions
    y_est_model <- predict(model, X_test)
  
    # Baseline model predictions
    #mean_value <- mean(X_test$WASO)
    #y_est_baseline <- data.frame(y_est_baseline = rep(mean_value, nrow(X_test)))
    model2 <- lmer("WASO ~ + (1 | id)", data = X_train)
    y_est_baseline <- predict(model2, X_test)
  
    # The true output values
    y_test <- X_test[11]
  
    # Save results
    y_model <- c(y_model, list(y_est_model))
    y_baseline <- c(y_baseline, y_est_baseline)
    y_true <- c(y_true, y_test)
    
  }
  
  # Convert lists to vectors
  y_model <- unlist(y_model)
  y_baseline <- unlist(y_baseline)
  y_true <- unlist(y_true)

  # Compute loss
  z_model <- abs(y_true - y_model)**2
  z_baseline <- abs(y_true - y_baseline)**2
  # Compute difference in loss
  z <- z_model - z_baseline
  
  # Compute p-value and CI for the differences between models
  t_test_result <- t.test(z, alternative = "two.sided", alpha = 0.05)
  
  # Save p-value and CI
  p_values_list[[j]] <- t_test_result$p.value
  estimates_list[[j]] <- t_test_result$estimate
  CI_list[[j]] <- t_test_result$conf.int
  
}

# Print result
for (j in 1:J) {
  cat(
    "Iteration", j, 
    ", estimate:", estimates_list[[j]],
    ", p-value:", p_values_list[[j]], 
    ", CI: [", CI_list[[j]][1], ",", CI_list[[j]][2], "]", 
    "\n"
  )
}


#########################################################

## Hold-out cross-validation
# 
# K = 50
# 
# seeds <- sample(1:1000, K, replace=FALSE)
# 
# # Initialize empty matrix and lists to store results
# r <- matrix(NA, 0, 1)
# p_values_list <- vector("list", K)
# estimates_list <- vector("list", K)
# 
# for (k in 1:K) {
#   
#   # Set seed to make sure we don't have the same partition twice
#   # set.seed(seeds[k])
#   
#   train_ind <- createDataPartition(y = X$WASO, p = 0.7, list = FALSE, groups = length(unique(X$id)))
#   
#   X_train <- X[train_ind, ]
#   X_test <- X[-train_ind, ]
#   
#   model <- lmer("WASO ~ cv + (1 | id)", data = X_train)
#   
#   y_est_model <- predict(model, X_test)
#   mean_value <- mean(X_test$WASO)
#   y_est_baseline <- data.frame(y_est_baseline = rep(mean_value, nrow(X_test)))
#   
#   y_test <- X_test[12]
#   
#   # Compute z with squared error.
#   zA <- abs(y_test - y_est_model)**2
#   zB <- abs(y_test - y_est_baseline)**2
#   z <- zA - zB
#   
#   r <- rbind(r, z)
#   
#   # Extract the p-value and estimate
#   p_values_list[[k]] <- t_test_result$p.value
#   estimates_list[[k]] <- t_test_result$estimate
# 
# }
# 
# # Confidence interval for model A (model)
# res <- t.test(zA, alternative = "two.sided", alpha = 0.05)
# (CIA <- c(res$conf.int[1], res$conf.int[2]))
# 
# # Confidence interval for model B (baseline)
# res <- t.test(zB, alternative = "two.sided", alpha = 0.05)
# (CIA <- c(res$conf.int[1], res$conf.int[2]))
# 
# # Perform the t-test
# t_test_result <- t.test(z, alternative = "two.sided", alpha = 0.05)
# 
# # Print p-values
# cat("p-values:\n")
# for (k in 1:K) {
#   cat("Iteration", k, ":", "p-value:", p_values_list[[k]], ", estimate:", estimates_list[[k]], "\n")
# }



