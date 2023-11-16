# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 14:17:28 2023

@author: LTEI0004
"""


#%%

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

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
# Predictions for the first dataset
predictions_1 = model_1.predict(sm.add_constant(data_1[['x']]))

# Fit a linear regression model for the second dataset
model_2 = sm.OLS(data_2['y'], sm.add_constant(data_2[['x']])).fit()
# Predictions for the second dataset
predictions_2 = model_2.predict(sm.add_constant(data_2[['x']]))


# Plotting the data points and single prediction line for each dataset
plt.figure(figsize=(10, 6))

# Plotting for dataset 1
plt.scatter(data_1['x'], data_1['y'], label='Individual 1', alpha=0.5, color='g')
plt.plot(data_1['x'], predictions_1, label='Prediction individual 1', color='g')

# Plotting for dataset 2
plt.scatter(data_2['x'], data_2['y'], label='Individual 2', alpha=0.5, color='m')
plt.plot(data_2['x'], predictions_2, label='Prediction individual 2', color='m')

plt.xlabel('x', fontname="Times New Roman", fontsize=18)
plt.ylabel('y', fontname="Times New Roman", fontsize=18)
plt.legend(fontsize=16)
plt.xticks(fontsize=16, family='Times New Roman')
plt.yticks(fontsize=16, family='Times New Roman')
plt.show()


# Combine data points from both datasets into a single dataframe
combined_data = pd.concat([data_1[['x', 'y']], data_2[['x', 'y']]])

# Fit a linear regression model for the combined data
model_combined = sm.OLS(combined_data['y'], sm.add_constant(combined_data['x'])).fit()
# Predictions for the combined data
predictions_combined = model_combined.predict(sm.add_constant(combined_data['x']))

# Plotting the combined data points and the true trend line for the combined data
plt.figure(figsize=(10, 6))

# Plotting combined data points
plt.scatter(combined_data['x'], combined_data['y'], label='Combined data for individual 1 and 2', alpha=0.5)

# Plotting the true trend line for the combined data
plt.plot(combined_data['x'], predictions_combined, color='r', linestyle='-', label='Prediction line for combined data')

plt.xlabel('x', fontname="Times New Roman", fontsize=18)
plt.ylabel('y', fontname="Times New Roman", fontsize=18)
plt.legend(fontsize=16)
plt.xticks(fontsize=16, family='Times New Roman')
plt.yticks(fontsize=16, family='Times New Roman')
plt.show()
