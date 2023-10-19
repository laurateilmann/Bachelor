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
from sklearn import model_selection


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

x_stan = zscore(x, ddof=1)
y = merged_data[['WASO']]
y_stan = zscore(y, ddof=1)




#%% Load the hourly data
cgm_hour = pd.read_csv(base_dir + '\concatenated_hourly_cgm.csv')
epochs_hour = pd.read_csv(base_dir + '\concatenated_hourly_epochs.csv')

# Merge the two dataframes based on common columns
merged_hour = pd.merge(cgm_hour, epochs_hour, on=['DateTime start'])

# Handling missing and infinite values
merged_hour.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_hour.dropna(inplace=True)

# Define the independent and dependent variables
xh = merged_hour.iloc[:, 2:12]

xh_stan = zscore(xh, ddof=1)
yh = merged_hour[['WASO']]
yh_stan = zscore(yh, ddof=1)


#%% Perform the multiple linear regression 
model_nightly = sm.OLS(y_stan, x_stan).fit()
model_hourly = sm.OLS(yh_stan, xh_stan).fit()

# Print the summary of the regression nightly
print(model_nightly.summary())

# Print the summary of the regression hourly
print(model_hourly.summary())


#%% Linear Regression model (in another way)

# Fit model
model_lm = lm.LinearRegression()
model_lm.fit(x_stan, y_stan)

#Estimate y values 
est_y = model_lm.predict(x_stan)

# Calculate residuals
residual = est_y - y_stan

#Scatter plot
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

# Histogram of residuals
plt.figure()
plt.hist(residual, bins=40)
plt.title(f"Histogram of the residual for {y.columns[0]}")

# Print model coefficients
print(model_lm.intercept_)
print(model_lm.coef_)

#%% Cross-validation to estimate generalization error

X = x_stan.values
Y = y_stan.values 

# Create crossvalidation partition for evaluation
K = 5
CV = model_selection.KFold(n_splits=K,shuffle=True)

Error_train = np.empty(K)
Error_test = np.empty(K)

k=0
for train_index, test_index in CV.split(X):
    print('Computing CV fold: {0}/{1}..'.format(k+1,K))

    # extract training and test set for current CV fold
    X_train, y_train = X[train_index,:], Y[train_index]
    X_test, y_test = X[test_index,:], Y[test_index]
    
    model_lm = lm.LinearRegression()
    model_lm.fit(X, Y)

    y_est_test = model_lm.predict(X_test)
    y_est_train = model_lm.predict(X_train)  

    # error_test = np.sum(np.square(y_est_test - y_test)) / float(len(y_est_test))
    # error_train = np.sum(y_est_train - y_train) / float(len(y_est_train))
    # Error_test[k], Error_train[k] = error_test, error_train    

    Error_train[k] = np.square(y_train-y_est_train).sum()/y_train.shape[0]
    Error_test[k] = np.square(y_test-y_est_test).sum()/y_test.shape[0]     
 
    k+=1

est_gen_error = Error_test.mean() 

#%% Basis model

# Generate random y values from a normal distribution N(0,1)
N = len(y_stan)
basis_mean = 0
basis_std = 1
basis_y = pd.DataFrame(basis_std*np.random.randn(N) + basis_mean, columns=["WASO"])

# Calculate residuals
basis_residual = basis_y - y_stan

#Scatter plot
data_min = -3
data_max = 4

plt.figure()
plt.plot(basis_y, est_y, ".")
plt.gca().set_aspect('equal')
plt.xlim(data_min, data_max)
plt.ylim(data_min, data_max)
plt.xlabel("True")
plt.ylabel("Estimated")
plt.title(f"Basis model: Estimated vs true values for {y.columns[0]}")

# Histogram of residuals
plt.figure()
plt.hist(basis_residual, bins=40)
plt.title(f"Basis model: Histogram of the residual for {y.columns[0]}")

#%% Cross-validation to estimate generalization error for basis model. OBS PROBABLY NOT WORKING!

X = x_stan.values
Y = y_stan.values 

# Create crossvalidation partition for evaluation
K = 5
CV = model_selection.KFold(n_splits=K,shuffle=True)

Error_train = np.empty(K)
Error_test = np.empty(K)

k=0
for train_index, test_index in CV.split(X):
    print('Computing CV fold: {0}/{1}..'.format(k+1,K))

    # extract training and test set for current CV fold
    X_train, y_train = X[train_index,:], Y[train_index]
    X_test, y_test = X[test_index,:], Y[test_index]
    
    N_test = len(y_test)
    N_train = len(y_train)
    basis_mean = 0
    basis_std = 1
    
    y_est_test = basis_std*np.random.randn(N_test) + basis_mean
    y_est_train = basis_std*np.random.randn(N_train) + basis_mean 

    Error_train[k] = np.square(y_train-y_est_train).sum()/y_train.shape[0]
    Error_test[k] = np.square(y_test-y_est_test).sum()/y_test.shape[0]        
 
    k+=1

est_gen_error_basis = Error_test.mean() 
