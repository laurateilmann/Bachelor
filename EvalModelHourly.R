
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
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_hourly_all_11.csv'), col_types = cols())

# Handling missing and infinite values
complete_dataset <- na.omit(complete_dataset)

# Define the independent and dependent variables
x <- complete_dataset %>% select(2:11)
y <- complete_dataset %>% select(WASO)

N <- nrow(x)
M <- ncol(x)

# Extract ID
Id <- complete_dataset %>% select(id)

# Standardize data
x_stan <- scale(x, center = TRUE, scale = TRUE)

# Include offset
x_stan <- cbind(1, x_stan)

# Create a new data frame combining x_stan and y_stan
X <- data.frame(x_stan, y, id=Id)

#########################################################

## Hold-out cross-validation

## Set the seed to make your partition reproducible
set.seed(123)
train_ind <- createDataPartition(y = X$WASO, p = 0.7, list = FALSE, groups = length(unique(X$id)))

X_train <- X[train_ind, ]
X_test <- X[-train_ind, ]

model <- lmer("WASO ~ cv + (1 | id)", data = X_train)

y_est_model <- predict(model, X_test)
mean_value <- mean(X_test$WASO)
y_est_baseline <- data.frame(y_est_baseline = rep(mean_value, nrow(X_test)))

y_test <- X_test[12]


# Compute z with squared error.
zA <- abs(y_test - y_est_model)**2
zB <- abs(y_test - y_est_baseline)**2
z <- zA - zB

# Confidence interval for model A (model)
res <- t.test(zA, alternative = "two.sided", alpha = 0.05)
(CIA <- c(res$conf.int[1], res$conf.int[2]))

# Confidence interval for model B (baseline)
res <- t.test(zA, alternative = "two.sided", alpha = 0.05)
(CIA <- c(res$conf.int[1], res$conf.int[2]))

# Compute confidence interval of z = zA-zB and p-value of Null hypothesis


t.test(z, alternative = "two.sided", alpha = 0.05)

###########################################################

## K-fold cross-validation

r <- matrix(NA, 0, 1)

K = 5
CV <- list()
CV$which <- createFolds(1:N, k = K, list = F)

for (k in 1:K) {
  
  # Extract training and test set
  X_train <- X[CV$which != k, ]
  X_test <- X[CV$which == k, ]
  
  model <- lmer("WASO ~ cv + (1 | id)", data = X_train)
  
  y_est_model <- predict(model, X_test)
  
  mean_value <- mean(X_test$WASO)
  y_est_baseline <- data.frame(y_est_baseline = rep(mean_value, nrow(X_test)))
  
  y_test <- X_test[12]
  
  zA <- abs(y_test - y_est_model)**2
  zB <- abs(y_test - y_est_baseline)**2
  z <- zA - zB
  
  r <- rbind(r, z)
}


# Compute confidence interval and p-value for the differences between models
t.test(z, alternative = "two.sided", alpha = 0.05)



