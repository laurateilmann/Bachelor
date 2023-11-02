# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 08:54:25 2023

@author: LTEI0004
"""


import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pylab as plt

# Set random seed for reproducibility
np.random.seed(0)

# Generate a synthetic dataset
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

#Scatter plot
data_min = -3
data_max = 4

plt.figure()
plt.plot(y, y_est, ".")
plt.plot(y, y, "-", label='True Trend', color='r')
plt.gca().set_aspect('equal')
plt.xlabel("True")
plt.ylabel("Estimated")
plt.title(f"True against estimated y values")


plt.figure()
plt.plot(X['Feature_1'], y, ".")
plt.plot(X['Feature_1'], X['Feature_1'] * coef[0], color='r', linestyle='-', label='First Coefficient')  
plt.xlabel("Feature 1")
plt.ylabel("y")
plt.title(f"Feature 1 against y")

# Histogram of residuals
plt.figure()
plt.hist(residual, bins=30)
plt.title(f"Histogram of the residuals")

# Print the coefficients and intercept from the regression model
print("Intercept from regression model:", model_lm.intercept_)
print("Coefficients from regression model:", model_lm.coef_)
