###############################################################################
# Authors: MGRO0154 & LTEI0004

# Use linear mixed effects regression to investigate the relationship between
# the response (nightly WASO, hourly WASO, Sleep Efficiency) and a sinlge
# predictor (BG parameters).
###############################################################################

# Load libraries
library(dplyr)
library(readr)
library(lme4)

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
y <- complete_dataset %>% select(WASO) # Change 'WASO' to 'Efficiency' when looking at Sleep Efficiency

# Standardize data
x_stan <- scale(x, center = TRUE, scale = TRUE)

# Extract ID
Id <- complete_dataset %>% select(id)

# Create a new data frame combining x_stan and y_stan
standardized_data <- data.frame(x_stan, y, id=Id)

# Number of observations
N = nrow(standardized_data)

for (var in var_names) {
  # Model
  formula <- as.formula(paste("WASO ~", var, "+ (1 | id)")) # Change 'WASO' to 'Efficiency' when looking at Sleep Efficiency
  model <- lmer(formula, data = standardized_data)
  print(summary(model))
  
  # p-value
  p <- round(2*pt(q=abs(coef(summary(model))[,3]), df=N-1, lower.tail=FALSE),3)
  p2 <- round(2*pnorm(abs(coef(summary(model))[,3]), lower.tail = FALSE),3)
  print('p-values:')
  print(p)
  print('p2-values:')
  print(p2)
  
  # CI
  conf_interval <- confint(model, level = 0.95)
  print(conf_interval)
}


#############################
## Hourly

# Load the hourly data
complete_dataset_h <- read_csv(file.path(base_dir, 'concatenated_hourly_all_11.csv'), col_types = cols())

# Handling missing and infinite values
complete_dataset_h <- na.omit(complete_dataset_h)

# Define the independent and dependent variables
x_h <- complete_dataset_h %>% select(2:11)
y_h <- complete_dataset_h %>% select(WASO)

# Standardize data
x_stan_h <- scale(x_h, center = TRUE, scale = TRUE)

# Extract ID
Id_h <- complete_dataset_h %>% select(id)

# Create a new data frame combining x_stan and y_stan
standardized_data_h <- data.frame(x_stan_h, y_h, id=Id_h)

# Number of observations
N_h = nrow(standardized_data)

for (var in var_names) {
  # Model
  formula <- as.formula(paste("WASO ~", var, "+ (1 | id)"))
  model_h <- lmer(formula, data = standardized_data_h)
  print(summary(model_h))
  
  # p-value
  p <- round(2*pt(q=abs(coef(summary(model_h))[,3]), df=N_h-1, lower.tail=FALSE),3)
  p2 <- round(2*pnorm(abs(coef(summary(model_h))[,3]), lower.tail = FALSE),3)
  print('p-values:')
  print(p)
  print('p2-values:')
  print(p2)
  
  # CI
  conf_interval <- confint(model_h, level = 0.95)
  print(conf_interval)
}



