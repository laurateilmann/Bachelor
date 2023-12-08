# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 14:17:28 2023

@author: LTEI0004
"""


#%% Import packages

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

# Close all figures
plt.close('all')

#%%

# Output directory for saving figures
out_dir = r"H:\GitHub\Bachelor\Plots"

# Generating the first dataset with individual variability
np.random.seed(123)
n = 400
group_1 = np.repeat(1, n)
x_1 = np.random.randn(n)
offset_1 = (2 + 0.8 * group_1 + np.random.uniform(-0.5, 0.5, n)) * x_1 + np.random.randn(n) * 0.3 * group_1
y_1 = 3 * x_1 + 7 + np.random.randn(n) + np.random.normal(0, 3, n)
data_1 = pd.DataFrame({'group': group_1, 'x': x_1, 'y': y_1, 'offset': offset_1})

# Generating the second dataset with individual variability
group_2 = np.repeat(2, n)
x_2 = np.random.randn(n)+3
offset_2 = (2 + 0.8 * group_2 + np.random.uniform(-0.5, 0.5, n)) * x_2 + np.random.randn(n) * 0.3 * group_2
y_2 = 3 * x_2 + 1 + np.random.randn(n) + np.random.normal(0, 2, n)
data_2 = pd.DataFrame({'group': group_2, 'x': x_2, 'y': y_2, 'offset': offset_2})

# Fit a linear regression model for the first dataset
model_1 = sm.OLS(data_1['y'], sm.add_constant(data_1[['x']])).fit()
# Model coefficients for the first dataset
coef_1 = model_1.params

# Fit a linear regression model for the second dataset
model_2 = sm.OLS(data_2['y'], sm.add_constant(data_2[['x']])).fit()
# Model coefficients for the second dataset
coef_2 = model_2.params


# Min and max values for plotting
min_val_x = min(min(x_1),min(x_2))-1
max_val_x = max(max(x_1),max(x_2))+1
min_val_y = min(min(y_1),min(y_2))-7
max_val_y = max(max(y_1),max(y_2))+2
# x-values for plotting prediction lines
x = np.linspace(min_val_x, max_val_x, 1000)


# Plotting the data points and single prediction line for each dataset
plt.figure(figsize=(15, 9))
# Plotting for dataset 1
plt.plot(data_1['x'], data_1['y'], ".", label='Individual 1', alpha=0.5, color='g', markersize=30)
plt.plot(x, coef_1[0] + coef_1[1]*x, label='Prediction individual 1', color='g', linewidth=5)
# Plotting for dataset 2
plt.plot(data_2['x'], data_2['y'], ".", label='Individual 2', alpha=0.5, color='m', markersize=30)
plt.plot(x, coef_2[0] + coef_2[1]*x, label='Prediction individual 2', color='m', linewidth=5)
# Plot settings
plt.xlabel('x', fontname="Times New Roman", fontsize=40)
plt.ylabel('y', fontname="Times New Roman", fontsize=40)
plt.legend(fontsize=33)
plt.xticks(fontsize=33, family='Times New Roman')
plt.yticks(fontsize=33, family='Times New Roman')
plt.xlim(min_val_x, max_val_x)
plt.ylim(min_val_y, max_val_y)
plt.tight_layout()
plt.show()
# Save fig
out_path = os.path.join(out_dir, 'LMM_offset.png')
plt.savefig(out_path)


# Combine data points from both datasets into a single dataframe
combined_data = pd.concat([data_1[['x', 'y']], data_2[['x', 'y']]])

# Fit a linear regression model for the combined data
model_combined = sm.OLS(combined_data['y'], sm.add_constant(combined_data['x'])).fit()
# Model coefficients for the combined dataset
coef_combined = model_combined.params

# Plotting the combined data points and the true trend line for the combined data
plt.figure(figsize=(15, 9))
# Plotting combined data points
plt.plot(combined_data['x'], combined_data['y'], ".", label='Combined data for individual 1 and 2', alpha=0.5, markersize=30)
plt.plot(x, coef_combined[0] + coef_combined[1]*x, label='Prediction line for combined data', color='r', linewidth=5)
# Figure settings
plt.xlabel('x', fontname="Times New Roman", fontsize=40)
plt.ylabel('y', fontname="Times New Roman", fontsize=40)
plt.legend(fontsize=33)
plt.xticks(fontsize=33, family='Times New Roman')
plt.yticks(fontsize=33, family='Times New Roman')
plt.xlim(min_val_x, max_val_x)
plt.ylim(min_val_y, max_val_y)
plt.tight_layout()
plt.show()
# Save fig
out_path = os.path.join(out_dir, 'LMM_combined.png')
plt.savefig(out_path)

