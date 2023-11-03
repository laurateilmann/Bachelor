# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 08:54:25 2023

@author: LTEI0004
"""

#%% Import packages
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pylab as plt

#%% Generate a random synthetic dataset 

#Set random seed for reproducibility
np.random.seed(0)

# Generate a synthetic dataset: intialize number of samples, feature and noise ratio
n_samples = 1000
n_features = 3
noise = 10

X, y, coef = make_regression(n_samples=n_samples, n_features=n_features, noise=noise, coef=True)

# Create a pandas DataFrame
df = pd.DataFrame(X, columns=['Feature_1', 'Feature_2', 'Feature_3'])
df['Target'] = y

# Perform multiple linear regression
X = df[['Feature_1', 'Feature_2', 'Feature_3']]
y = df['Target']

# Create and fit the linear regression model
model_lm = LinearRegression()
model_lm.fit(X, y)

#Estimate y values 
y_est = model_lm.predict(X)

# Calculate residuals
residual = y_est - y

# Settings for data
data_min = -3
data_max = 4

plt.rcParams["font.family"] = "Times New Roman"

#Scatter plot med trend line
plt.figure()
plt.plot(y, y_est, ".")
plt.plot(y, y, "-", label='True Trend', color='r')
plt.gca().set_aspect('equal')
plt.xlabel("True", fontname="Times New Roman", fontsize=14)
plt.ylabel("Estimated", fontname="Times New Roman", fontsize=14)
plt.title(f"True against estimated y values", fontname="Times New Roman", fontsize=16)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')

# Independent variable plotted and true correlation line
plt.figure()
plt.plot(X['Feature_1'], y, ".", label='Data points')
plt.plot(X['Feature_1'], X['Feature_1'] * coef[0], color='r', linestyle='-', label='True correlation') 
plt.xlabel("Feature 1", fontname="Times New Roman", fontsize=14)
plt.ylabel("y", fontname="Times New Roman", fontsize=14)
plt.legend(fontsize=14)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')

plt.figure()
plt.plot(X['Feature_2'], y, ".", label='Data points')
plt.plot(X['Feature_2'], X['Feature_2'] * coef[1], color='r', linestyle='-', label='True correlation') 
plt.xlabel("Feature 2", fontname="Times New Roman", fontsize=14)
plt.ylabel("y", fontname="Times New Roman", fontsize=14)
plt.legend(fontsize=14)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')

plt.figure()
plt.plot(X['Feature_3'], y, ".", label='Data points')
plt.plot(X['Feature_3'], X['Feature_3'] * coef[2], color='r', linestyle='-', label='True correlation') 
plt.xlabel("Feature 3", fontname="Times New Roman", fontsize=14)
plt.ylabel("y", fontname="Times New Roman", fontsize=14)
plt.legend(fontsize=14)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')

# Histogram of residuals
plt.figure()
plt.hist(residual, bins=30)
plt.title(f"Histogram of the residuals", fontname="Times New Roman", fontsize=16)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')

# Print the coefficients and intercept from the regression model
print("Intercept from regression model:", model_lm.intercept_)
print("Coefficients from regression model:", model_lm.coef_)
