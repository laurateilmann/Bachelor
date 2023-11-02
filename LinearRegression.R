
# Load libraries
library(dplyr)
library(readr)
library(zoo)
library(lme4)
library(stats)
library(olsrr)

# Set your base directory
base_dir <- "L:/LovbeskyttetMapper01/StenoSleepQCGM"

# Load the nightly data
complete_dataset <- read_csv(file.path(base_dir, 'concatenated_all.csv'), col_types = cols())

# Handling missing and infinite values
complete_dataset <- na.omit(complete_dataset)

# Define the independent and dependent variables
x <- complete_dataset %>% select(3:12)
y <- complete_dataset %>% select(WASO)

# Standardize data
x_stan <- scale(x, center = TRUE, scale = TRUE)
y_stan <- scale(y, center = TRUE, scale = TRUE)

# Include offset
x_stan <- cbind(1, x_stan)

# Extract ID
Id <- complete_dataset %>% select(id)

# Create a new data frame combining x_stan and y_stan
standardized_data <- data.frame(x_stan, y_stan, id=Id)

# Model
model <- lmer(WASO ~ TIR + TAR + TBR + min + max + mean + median + std + cv + delta.IG + (1 | id), data = standardized_data)
summary(model)

# p-value
p = round(2*pnorm(abs(coef(summary(model))[,3]), lower.tail = FALSE),3)
print(p)

#################

# forward selection
modelf <- lm(WASO ~ TIR + TAR + min + max + mean + std + delta.IG, data = standardized_data)
final_model <- ols_step_all_possible(modelf)
print(final_model)
 




