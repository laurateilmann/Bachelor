# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:26:04 2023

@author: LTEI0004
"""

#%% Import packages
import pandas as pd
from datetime import datetime
from ExtractIntervals import extract_one_night
import numpy as np
import os
from ActiFeaturesFunc import *
import csv
from PlotFunc import *
import plotly.io as io
from ExtractIntervals import *
import plotly.graph_objects as go
import plotly.io as io
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from mpl_toolkits.mplot3d import Axes3D

plt.close('all')

#%% Import concatenated data

base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data"

# File name
file = "\concatenated_all_11.csv"

# Construct the full file paths
file_path = os.path.join(base_dir+file)

# Read the cgm and epoch data
feature_df = pd.read_csv(file_path)

#%% CV and Sleep Efficiency

plt.figure()
plt.plot(feature_df['cv'], feature_df['Efficiency'], 'o', label='Data Points', alpha=0.5)
plt.title("Sleep Efficiency against CV", fontsize=16, family='Times New Roman')
plt.xlabel("CV", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\CV against Sleep Efficiency.png", format="png")


#%% Plot: TIR and Sleep Efficiency

plt.figure()
plt.plot(feature_df['TIR'], feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against TIR", fontsize=16, family='Times New Roman')
plt.xlabel("TIR (%)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\TIR against Sleep Efficiency.png", format="png")   

#%% Plot: TAR and Sleep Efficiency

plt.figure()
plt.plot(feature_df['TAR'], feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against TAR", fontsize=16, family='Times New Roman')
plt.xlabel("TAR (%)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\TAR against Sleep Efficiency.png", format="png") 

#%% Plot: TBR and Sleep Efficiency

plt.figure()
plt.plot(feature_df['TBR'], feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against TBR", fontsize=16, family='Times New Roman')
plt.xlabel("TBR (%)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\TBR against Sleep Efficiency.png", format="png") 

#%% Plot: max IG and Sleep Efficiency

plt.figure()
plt.plot(feature_df['max'], feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against Max BG", fontsize=16, family='Times New Roman')
plt.xlabel("Max BG (mmol/L)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)",fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\Max against Sleep Efficiency.png", format="png")   

#%% Plot: min IG and Sleep Efficiency

plt.figure()
plt.plot(feature_df['min'], feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against Min BG", fontsize=16, family='Times New Roman')
plt.xlabel("Min BG (mmol/L)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\Min against Sleep Efficiency.png", format="png")   

#%% Mean and Sleep Efficiency

plt.figure()
plt.plot(feature_df['mean'], feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against Mean BG", fontsize=16, family='Times New Roman')
plt.xlabel("Mean BG (mmol/L)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\Mean against Sleep Efficiency.png", format="png") 

#%% 3D plot with Min and Max BG

# Extracting data
max_bg = feature_df['max']
min_bg = feature_df['min']
sleep_efficiency = feature_df['Efficiency']

# Creating a 3D plot
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot points
ax.scatter(max_bg, min_bg, sleep_efficiency, marker='o', alpha=0.9)

# Prediction plane equation parameters
# Creating a meshgrid for the prediction plane
max_bg_range = np.linspace(min(max_bg), max(max_bg), 100)
min_bg_range = np.linspace(min(min_bg), max(min_bg), 100)
X, Y = np.meshgrid(max_bg_range, min_bg_range)
Z = 81.05 - 1.62 * X + 0.99 * Y  # Prediction plane equation from R

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
plt.savefig(f"H:\GitHub\Bachelor\Plots\Plot 3D Efficiency.png", format="png") 
plt.show()

