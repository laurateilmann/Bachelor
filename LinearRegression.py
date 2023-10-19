# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 09:55:11 2023

@author: ltei0004
"""


import pandas as pd
import numpy as np
import statsmodels.api as sm
import sklearn.linear_model as lm
import matplotlib.pylab as plt
from scipy.stats import zscore
from sklearn.preprocessing import StandardScaler

base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM"

# Load the data
cgm_data = pd.read_csv(base_dir + '\concatenated_cgm.csv')
epochs_data = pd.read_csv(base_dir + '\concatenated_epochs.csv')

# Merge the two dataframes based on common columns
merged_data = pd.merge(cgm_data, epochs_data, on=['In Bed DateTime', 'Out Bed DateTime'])

# Handling missing and infinite values
merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_data.dropna(inplace=True)

# Define the independent and dependent variables
x = merged_data.iloc[:, 2:12]

x_stan = zscore(x, ddof=1)
y = merged_data[['WASO']]
y_stan = zscore(y, ddof=1)

# Add a constant column to the independent variables
x_stan = sm.add_constant(x_stan)


#%% Perform the multiple linear regression
model = sm.OLS(y_stan, x_stan).fit()

# Print the summary of the regression
print(model.summary())


#%% Linear Regression model 

model_lm = lm.LinearRegression()
model_lm.fit(x_stan, y_stan)

#Estimate 
est_y = model_lm.predict(x_stan)

residual = est_y - y_stan

#Scatter plot and histogram
data_min = -3
data_max = 4

plt.figure()
plt.plot(y_stan, est_y, ".")
plt.gca().set_aspect('equal')
plt.xlim(data_min, data_max)
plt.ylim(data_min, data_max)
plt.xlabel("True")
plt.ylabel("Estimated")
plt.title(f"Estimated vs true values for {y.columns[0]}")

plt.figure()
plt.hist(residual, bins=40)
plt.title(f"Histogram of the residual for {y.columns[0]}")

print(model_lm.intercept_)
print(model_lm.coef_)
