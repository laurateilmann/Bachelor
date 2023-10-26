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
from sklearn import model_selection, linear_model


base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM"

#%% Load the nightly data
cgm_data = pd.read_csv(base_dir + '\concatenated_cgm.csv')
epochs_data = pd.read_csv(base_dir + '\concatenated_epochs.csv')

# Merge the two dataframes based on common columns
merged_data = pd.merge(cgm_data, epochs_data, on=['In Bed DateTime', 'Out Bed DateTime'])

# Handling missing and infinite values
merged_data.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_data.dropna(inplace=True)

# Define the independent and dependent variables
x = merged_data.iloc[:, 2:12]
y = merged_data[['WASO']]

# Standardize data
x_stan = zscore(x, ddof=1)
y_stan = zscore(y, ddof=1)

# Include offset
x_stan = sm.add_constant(x_stan)

#%% Load the hourly data
cgm_hour = pd.read_csv(base_dir + '\concatenated_hourly_cgm.csv')
epochs_hour = pd.read_csv(base_dir + '\concatenated_hourly_epochs.csv')

# Merge the two dataframes based on common columns
merged_hour = pd.merge(cgm_hour, epochs_hour, on=['DateTime start'])

# Handling missing and infinite values
merged_hour.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_hour.dropna(inplace=True)

# Define the independent and dependent variables
xh = merged_hour.iloc[:, 1:11]
yh = merged_hour[['WASO']]

# Standardize data
xh_stan = zscore(xh, ddof=1)
yh_stan = zscore(yh, ddof=1)

# Include offset
xh_stan = sm.add_constant(xh_stan)

#%% Perform the multiple linear regression 
model_nightly = sm.OLS(y_stan, x_stan).fit()
model_hourly = sm.OLS(yh_stan, xh_stan).fit()

# Print the summary of the regression nightly
print(model_nightly.summary())

# Print the summary of the regression hourly
print(model_hourly.summary())


#%% Linear Regression model (in another way) (nightly)

# Fit model
model_lm = lm.LinearRegression()
model_lm.fit(x_stan, y_stan)

#Estimate y values 
y_est = model_lm.predict(x_stan)

# Calculate residuals
residual = y_est - y_stan

#Scatter plot
data_min = -3
data_max = 4

plt.figure()
plt.plot(y_stan, y_est, ".")
plt.gca().set_aspect('equal')
plt.xlim(data_min, data_max)
plt.ylim(data_min, data_max)
plt.xlabel("True")
plt.ylabel("Estimated")
plt.title(f"Estimated vs true values for {y.columns[0]}")

# Histogram of residuals
plt.figure()
plt.hist(residual, bins=30)
plt.title(f"Histogram of the residual for {y.columns[0]}")

# Print model coefficients
print(model_lm.intercept_)
print(model_lm.coef_)

# Plot baseline model (mean of target variable)
y_mean = y_stan.iloc[:]['WASO'].mean()
y_baseline = pd.DataFrame({'WASO': [y_mean] * len(y_stan)})
plt.figure()
plt.plot(y_stan, y_baseline, ".")
plt.gca().set_aspect('equal')
plt.xlim(data_min, data_max)
plt.ylim(data_min, data_max)
plt.xlabel("True")
plt.ylabel("Estimated")
plt.title(f"Estimated vs true values for {y.columns[0]} (baseline)")

# Histogram of residuals
residual_baseline = y_baseline - y_stan
plt.figure()
plt.hist(residual_baseline, bins=30)
plt.title(f"Histogram of the residual for {y.columns[0]} (baseline)")

#%% Linear Regression model (in another way) (hourly)

# Fit model
model_lm = lm.LinearRegression()
model_lm.fit(xh_stan, yh_stan)

#Estimate y values 
yh_est = model_lm.predict(xh_stan)

# Calculate residuals
residual = yh_est - yh_stan

#Scatter plot
data_min = -3
data_max = 4

plt.figure()
plt.plot(yh_stan, yh_est, ".")
plt.gca().set_aspect('equal')
plt.xlim(data_min, data_max)
plt.ylim(data_min, data_max)
plt.xlabel("True")
plt.ylabel("Estimated")
plt.title(f"Estimated vs true values for hourly {y.columns[0]}")

# Histogram of residuals
plt.figure()
plt.hist(residual, bins=30)
plt.title(f"Histogram of the residual for hourly {y.columns[0]}")

# Print model coefficients
print(model_lm.intercept_)
print(model_lm.coef_)

# Plot baseline model (mean of target variable)
yh_mean = yh_stan.iloc[:]['WASO'].mean()
yh_baseline = pd.DataFrame({'WASO': [yh_mean] * len(yh_stan)})
plt.figure()
plt.plot(yh_stan, yh_baseline, ".")
plt.gca().set_aspect('equal')
plt.xlim(data_min, data_max)
plt.ylim(data_min, data_max)
plt.xlabel("True")
plt.ylabel("Estimated")
plt.title(f"Estimated vs true values for hourly {y.columns[0]} (baseline)")

# Histogram of residuals
residual_baseline = yh_baseline - yh_stan
plt.figure()
plt.hist(residual_baseline, bins=30)
plt.title(f"Histogram of the residual for hourly {y.columns[0]} (baseline)")

#%% Cross-validation to estimate generalization error (nightly)

# Extract x and y values from dataframes
X = x_stan.values
Y = y_stan.values 

# Create crossvalidation partition for evaluation
K = 5
CV = model_selection.KFold(n_splits=K,shuffle=True)

# Create empty arrays for storing test and training errors
Error_train = np.empty(K)
Error_test = np.empty(K)
Error_train_baseline = np.empty((K,1))
Error_test_baseline = np.empty((K,1))

k=0
for train_index, test_index in CV.split(X):
    print('Computing CV fold: {0}/{1}..'.format(k+1,K))

    # Extract training and test set for current CV fold
    X_train, y_train = X[train_index,:], Y[train_index]
    X_test, y_test = X[test_index,:], Y[test_index]
    
    # Fit linear regression model
    model_lm = lm.LinearRegression()
    model_lm.fit(X_train, y_train)

    # Predict
    y_est_train = model_lm.predict(X_train) 
    y_est_test = model_lm.predict(X_test)   
    
    # MSE of baseline model (mean of target variable)
    Error_train_baseline[k] = np.square(y_train-y_train.mean()).sum()/y_train.shape[0]
    Error_test_baseline[k] = np.square(y_test-y_test.mean()).sum()/y_test.shape[0]
    
    # MSE of linear regression model
    Error_train[k] = np.square(y_train-y_est_train).sum()/y_train.shape[0]
    Error_test[k] = np.square(y_test-y_est_test).sum()/y_test.shape[0]     
 
    k+=1

# Estimate generalization errors
est_gen_error = Error_test.mean() 
est_gen_error_baseline = Error_test_baseline.mean()

#%% Cross-validation to estimate generalization (hourly)

# Extract x and y values from dataframes
X = xh_stan.values
Y = yh_stan.values 

# Create crossvalidation partition for evaluation
K = 10
CV = model_selection.KFold(n_splits=K,shuffle=True)

# Create empty arrays for storing test and training errors
Error_train = np.empty(K)
Error_test = np.empty(K)
Error_train_baseline = np.empty((K,1))
Error_test_baseline = np.empty((K,1))

k=0
for train_index, test_index in CV.split(X):
    print('Computing CV fold: {0}/{1}..'.format(k+1,K))

    # Extract training and test set for current CV fold
    X_train, y_train = X[train_index,:], Y[train_index]
    X_test, y_test = X[test_index,:], Y[test_index]
    
    # Fit linear regression model
    model_lm = lm.LinearRegression()
    model_lm.fit(X_train, y_train)

    # Predict
    y_est_train = model_lm.predict(X_train) 
    y_est_test = model_lm.predict(X_test)   
    
    # MSE of baseline model (mean of target variable)
    Error_train_baseline[k] = np.square(y_train-y_train.mean()).sum()/y_train.shape[0]
    Error_test_baseline[k] = np.square(y_test-y_test.mean()).sum()/y_test.shape[0]
    
    # MSE of linear regression model
    Error_train[k] = np.square(y_train-y_est_train).sum()/y_train.shape[0]
    Error_test[k] = np.square(y_test-y_est_test).sum()/y_test.shape[0]     
 
    k+=1

# Estimate generalization errors
est_gen_error = Error_test.mean() 
est_gen_error_baseline = Error_test_baseline.mean()

