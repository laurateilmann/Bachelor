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
df = pd.DataFrame(X, columns=['x1', 'x2', 'x3'])
df['Target'] = y

# Perform multiple linear regression
X = df[['x1', 'x2', 'x3']]
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

# Min and max values for plotting
min_val_x = min(X['x1'])-0.5
max_val_x = max(X['x1'])+0.5
min_val_y = min(y)-50
max_val_y = max(y)+50
# x-values and y-values for plotting lines
x_line = np.linspace(min_val_x, max_val_x, 1000)
y_line = np.linspace(min_val_y, max_val_y, 1000)

# Font in plots
plt.rcParams["font.family"] = "Times New Roman"

#%% True vs. estimated response values

plt.figure(figsize=(10,10))
plt.plot(y, y_est, ".", label='Data points', alpha=0.5, markersize=30)
plt.plot(y_line, y_line, "-", label='Perfect fit', color='r', linewidth=5)
plt.gca().set_aspect('equal')
plt.xlabel("True", fontname="Times New Roman", fontsize=45)
plt.ylabel("Estimated", fontname="Times New Roman", fontsize=45)
plt.title(f"Estimated against true y values", fontname="Times New Roman", fontsize=47)
plt.xticks(fontsize=40, family='Times New Roman')
plt.yticks(fontsize=40, family='Times New Roman')
plt.legend(fontsize=40)
plt.xlim(min_val_y, max_val_y)
plt.ylim(min_val_y, max_val_y)
plt.tight_layout()
# Save fig
out_path = os.path.join(out_dir, 'Synthetic_true_vs_estimated.png')
plt.savefig(out_path)


#%% Response against x1 as well as true correlation line

plt.figure(figsize=(15,10))
plt.plot(X['x1'], y, ".", label='Data points', alpha=0.5, markersize=30)
plt.plot(x_line, x_line * coef[0], color='r', linestyle='-', label='True correlation', linewidth=5) 
plt.xlabel("x1", fontname="Times New Roman", fontsize=45)
plt.ylabel("y", fontname="Times New Roman", fontsize=45)
plt.title(f"y against x1", fontname="Times New Roman", fontsize=47)
plt.legend(fontsize=38)
plt.xticks(fontsize=38, family='Times New Roman')
plt.yticks(fontsize=38, family='Times New Roman')
plt.xlim(min_val_x, max_val_x)
plt.ylim(min_val_y, max_val_y)
plt.tight_layout()
# Save fig
out_path = os.path.join(out_dir, 'Synthetic_Feature1.png')
plt.savefig(out_path)

#%% Response against x2 as well as true correlation line

plt.figure()
plt.plot(X['x2'], y, ".", label='Data points', alpha=0.5)
plt.plot(X['x2'], X['x2'] * coef[1], color='r', linestyle='-', label='True correlation') 
plt.xlabel("x2 2", fontname="Times New Roman", fontsize=14)
plt.ylabel("y", fontname="Times New Roman", fontsize=14)
plt.legend(fontsize=14)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
plt.tight_layout()

#%% Response against x3 as well as true correlation line

plt.figure()
plt.plot(X['x3'], y, ".", label='Data points', alpha=0.5)
plt.plot(X['x3'], X['x3'] * coef[2], color='r', linestyle='-', label='True correlation') 
plt.xlabel("x3 3", fontname="Times New Roman", fontsize=14)
plt.ylabel("y", fontname="Times New Roman", fontsize=14)
plt.legend(fontsize=14)
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
plt.tight_layout()

#%% Histogram of residuals

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


