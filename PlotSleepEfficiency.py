# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:26:04 2023

@author: LTEI0004 & MGRO0154

Sleep Efficiency plotted against various BG parameters.
"""

#%% Import packages
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

#%% Close all figures

plt.close('all')

#%% Import concatenated data

# Base directory
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data"

# File name
file = "\concatenated_all_11.csv"

# Construct the full file path
file_path = os.path.join(base_dir+file)

# Read the cgm and epoch data
feature_df = pd.read_csv(file_path)

#%% Plotting settings

markersize = 20
title_size = 55
labelsize = 50
ticksize = 45
padsize = 20

#%% Plot: CV and Sleep Efficiency

plt.figure(figsize=(15, 10))
plt.plot(feature_df['cv'], feature_df['Efficiency'], 'o', label='Data Points', alpha=0.5, markersize=markersize)
plt.title("Sleep Efficiency against CV", fontsize=title_size, family='Times New Roman')
plt.xlabel("CV", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("Sleep Efficiency (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()

# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\Sleep Efficiency against CV.png", format="png")

#%% Plot: TIR and Sleep Efficiency

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TIR'], feature_df['Efficiency'], 'o', alpha=0.5, markersize=markersize)
plt.title("Sleep Efficiency against TIR", fontsize=title_size, family='Times New Roman')
plt.xlabel("TIR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("Sleep Efficiency (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()

# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\Sleep Efficiency against TIR.png", format="png")   

#%% Plot: TAR and Sleep Efficiency

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TAR'], feature_df['Efficiency'], 'o', alpha=0.5, markersize=markersize)
plt.title("Sleep Efficiency against TAR", fontsize=title_size, family='Times New Roman')
plt.xlabel("TAR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("Sleep Efficiency (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()

# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\Sleep Efficiency against TAR.png", format="png") 

#%% Plot: TBR and Sleep Efficiency

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TBR'], feature_df['Efficiency'], 'o', alpha=0.5, markersize=markersize)
plt.title("Sleep Efficiency against TBR", fontsize=title_size, family='Times New Roman')
plt.xlabel("TBR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("Sleep Efficiency (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()

# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\Sleep Efficiency against TBR.png", format="png") 

#%% Plot: Max BG and Sleep Efficiency

plt.figure(figsize=(15, 10))
plt.plot(feature_df['max'], feature_df['Efficiency'], 'o', alpha=0.5, markersize=markersize)
plt.title("Sleep Efficiency against Max BG", fontsize=title_size, family='Times New Roman')
plt.xlabel("Max BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("Sleep Efficiency (%)",fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()

# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\Sleep Efficiency against Max.png", format="png")   

#%% Plot: Min BG and Sleep Efficiency

plt.figure(figsize=(15, 10))
plt.plot(feature_df['min'], feature_df['Efficiency'], 'o', alpha=0.5, markersize=markersize)
plt.title("Sleep Efficiency against Min BG", fontsize=title_size, family='Times New Roman')
plt.xlabel("Min BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("Sleep Efficiency (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()

# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\Sleep Efficiency against Min.png", format="png")   

#%% Mean BG and Sleep Efficiency

plt.figure(figsize=(15, 10))
plt.plot(feature_df['mean'], feature_df['Efficiency'], 'o', alpha=0.5, markersize=markersize)
plt.title("Sleep Efficiency against Mean BG", fontsize=title_size, family='Times New Roman')
plt.xlabel("Mean BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("Sleep Efficiency (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()

# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\Sleep Efficiency against Mean.png", format="png") 

#%% 3D plot with Min and Max BG (Model_SE)

# Extracting data
max_bg = feature_df['max']
min_bg = feature_df['min']
sleep_efficiency = feature_df['Efficiency']

# Standardizing Min and Max BG values
scaler = StandardScaler()
max_bg_standardized = scaler.fit_transform(max_bg.values.reshape(-1, 1))
min_bg_standardized = scaler.fit_transform(min_bg.values.reshape(-1, 1))

# Creating a 3D plot
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
ax.scatter(max_bg_standardized, min_bg_standardized, sleep_efficiency, marker='o', alpha=1)

# Prediction plane equation parameters
# Creating a meshgrid for the prediction plane
max_bg_range = np.linspace(min(max_bg_standardized), max(max_bg_standardized), 100)
min_bg_range = np.linspace(min(min_bg_standardized), max(min_bg_standardized), 100)
X, Y = np.meshgrid(max_bg_range, min_bg_range)
# Prediction plane equation from R
Z = 81.05 - 1.62 * X + 0.99 * Y  

# Plotting the prediction plane
ax.plot_surface(X, Y, Z, alpha=0.5, color='red')

# Set labels and title with specified font and font size
label_font = {'fontsize': 40, 'family': 'Times New Roman'}
title_font = {'fontsize': 40, 'family': 'Times New Roman'}

ax.set_xlabel('Max BG (mmol/L)', fontdict=label_font, labelpad = 30)
ax.set_ylabel('Min BG (mmol/L)', fontdict=label_font, labelpad = 30)
ax.set_zlabel('Sleep Efficiency (%)', fontdict=label_font, labelpad = 30)

# Adjusting tick label font and size
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(35)
    tick.label.set_fontname('Times New Roman')

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(35)
    tick.label.set_fontname('Times New Roman')

for tick in ax.zaxis.get_major_ticks():
    tick.label.set_fontsize(35)
    tick.label.set_fontname('Times New Roman')
    
plt.tight_layout()
# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\Sleep Efficiency 3D plot.png", format="png") 
# Display fig
plt.show()

