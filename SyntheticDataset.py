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
import os

# Close all figures
plt.close('all')

#%% Generate a random synthetic dataset 

# Output directory for saving figures
out_dir = r"H:\GitHub\Bachelor\Plots"

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

# Print the coefficients and intercept from the regression model
print("Intercept from regression model:", model_lm.intercept_)
print("Coefficients from regression model:", model_lm.coef_)

#Estimate y values 
y_est = model_lm.predict(X)

# Calculate residuals
residual = y_est - y

# Settings for data
plt.rcParams["font.family"] = "Times New Roman"

# True vs. estimated response values
plt.figure(figsize=(10,10))
plt.plot(y, y_est, ".", label='Data points', alpha=0.5, markersize=30)
plt.plot(y, y, "-", label='Perfect fit', color='r', linewidth=5)
plt.gca().set_aspect('equal')
plt.xlabel("True", fontname="Times New Roman", fontsize=45)
plt.ylabel("Estimated", fontname="Times New Roman", fontsize=45)
plt.title(f"Estimated against true y values", fontname="Times New Roman", fontsize=47)
plt.xticks(fontsize=40, family='Times New Roman')
plt.yticks(fontsize=40, family='Times New Roman')
plt.legend(fontsize=40)
plt.tight_layout()
# Save fig
out_path = os.path.join(out_dir, 'Synthetic_true_vs_estimated.png')
plt.savefig(out_path)

# Response against Feature 1 as well as true correlation line
plt.figure(figsize=(15,10))
plt.plot(X['Feature_1'], y, ".", label='Data points', alpha=0.5, markersize=30)
plt.plot(X['Feature_1'], X['Feature_1'] * coef[0], color='r', linestyle='-', label='True correlation', linewidth=5) 
plt.xlabel("Feature 1", fontname="Times New Roman", fontsize=45)
plt.ylabel("y", fontname="Times New Roman", fontsize=45)
plt.title(f"y against Feature 1", fontname="Times New Roman", fontsize=47)
plt.legend(fontsize=38)
plt.xticks(fontsize=38, family='Times New Roman')
plt.yticks(fontsize=38, family='Times New Roman')
plt.tight_layout()
# Save fig
out_path = os.path.join(out_dir, 'Synthetic_Feature1.png')
plt.savefig(out_path)

# Response against Feature 2 as well as true correlation line
plt.figure()
plt.plot(X['Feature_2'], y, ".", label='Data points', alpha=0.5)
plt.plot(X['Feature_2'], X['Feature_2'] * coef[1], color='r', linestyle='-', label='True correlation') 
plt.xlabel("Feature 2", fontname="Times New Roman", fontsize=14)
plt.ylabel("y", fontname="Times New Roman", fontsize=14)
plt.legend(fontsize=14)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
plt.tight_layout()

# Response against Feature 3 as well as true correlation line
plt.figure()
plt.plot(X['Feature_3'], y, ".", label='Data points', alpha=0.5)
plt.plot(X['Feature_3'], X['Feature_3'] * coef[2], color='r', linestyle='-', label='True correlation') 
plt.xlabel("Feature 3", fontname="Times New Roman", fontsize=14)
plt.ylabel("y", fontname="Times New Roman", fontsize=14)
plt.legend(fontsize=14)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
plt.tight_layout()

# Histogram of residuals
plt.figure(figsize=(12,10))
plt.hist(residual, bins=30)
plt.title(f"Histogram of the residuals", fontname="Times New Roman", fontsize=47)
plt.xlabel("Residuals", fontname="Times New Roman", fontsize=45)
plt.ylabel("Frequency", fontname="Times New Roman", fontsize=45)
plt.xticks(fontsize=40, family='Times New Roman')
plt.yticks(fontsize=40, family='Times New Roman')
plt.tight_layout()
# Save fig
out_path = os.path.join(out_dir, 'Synthetic_histogram.png')
plt.savefig(out_path)


