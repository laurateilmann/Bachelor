# Load necessary libraries
library(lme4)
library(ggplot2)
library(ggeffects)
library(dplyr)
library(tidyr)

# Generating synthetic data for patients with unique IDs
set.seed(123)
num_patients <- 50
num_measurements <- 5

# Creating patient IDs and their corresponding measurements
patient_data <- data.frame(
  patient_id = rep(1:num_patients, each = num_measurements),
  measurement = rep(1:num_measurements, times = num_patients),
  bodyLength2 = rnorm(num_patients * num_measurements),
  mountainRange = factor(rep(1:3, length.out = num_patients * num_measurements))
)

# Generating random effects (individual patient intercepts)
patient_data$random_effect <- rnorm(nrow(patient_data), 0, 0.5)

# Generating outcome variable (test scores)
patient_data$testScore <- 3 * patient_data$bodyLength2 + patient_data$random_effect + rnorm(nrow(patient_data), 0, 0.5)

# Fitting a linear mixed effects model with random intercept for patient_id
mixed_model <- lmer(testScore ~ bodyLength2 + mountainRange + (1 | patient_id), data = patient_data)

# Extracting predicted values for random effects
predicted_values <- ggpredict(mixed_model, terms = c("bodyLength2", "mountainRange"), type = "re")

# Plotting individual intercepts based on patient IDs along with data points
plot(predicted_values) +
  geom_point(data = patient_data, aes(x = bodyLength2, y = testScore, color = as.factor(patient_id)), alpha = 0.5) +
  labs(x = "Body Length", y = "Predicted Test Score", 
       title = "Individual Intercept Effects based on Patient IDs with Data Points") +
  theme_minimal()
