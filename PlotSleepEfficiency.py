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

plt.close('all')

#%% Import concatenated data

base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data"

cgm_file = "\concatenated_cgm.csv"
epoch_file = "\concatenated_epochs.csv"

# Construct the full file paths
cgm_file_path = os.path.join(base_dir+cgm_file)
epoch_file_path = os.path.join(base_dir+epoch_file)

# Read the cgm and epoch data
cgm_feature_df = pd.read_csv(cgm_file_path)
epochs_feature_df = pd.read_csv(epoch_file_path)


#%% Plot: CV and Sleep Efficiency with trend

# Standardizing the data
cv_mean = cgm_feature_df['cv'].mean()
cv_std = cgm_feature_df['cv'].std()
cgm_feature_df['cv_standardized'] = (cgm_feature_df['cv'] - cv_mean) / cv_std

# Using the standardized column for the prediction
x = np.linspace(min(cgm_feature_df['cv_standardized']), max(cgm_feature_df['cv_standardized']), 1000)
y_pred = 80.9312 - 1.0440 * x

# Plotting the data
plt.figure()
plt.plot(cgm_feature_df['cv_standardized'], epochs_feature_df['Efficiency'], 'o', label='Data Points', alpha=0.5)
plt.plot(x, y_pred, '-', label='Prediction Line', color='red', linewidth=2)
plt.title("Sleep Efficiency against CV", fontsize=16, family='Times New Roman')
plt.xlabel("CV", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
legend_font = {'family': 'Times New Roman', 'size': 12}
plt.legend(prop=legend_font)
plt.show()

plt.savefig(f"H:\GitHub\Bachelor\Plots\CV vs. Sleep Efficiency with trend.png", format="png")

#%% CV and Sleep Efficiency

plt.figure()
plt.plot(cgm_feature_df['cv_standardized'], epochs_feature_df['Efficiency'], 'o', label='Data Points', alpha=0.5)
plt.title("Sleep Efficiency against CV", fontsize=16, family='Times New Roman')
plt.xlabel("CV", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\CV against Sleep Efficiency.png", format="png")


#%% Plot: TIR and Sleep Efficiency

plt.figure()
plt.plot(cgm_feature_df['TIR'], epochs_feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against TIR", fontsize=16, family='Times New Roman')
plt.xlabel("TIR (%)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\TIR against Sleep Efficiency.png", format="png")   

#%% Plot: TAR and Sleep Efficiency

plt.figure()
plt.plot(cgm_feature_df['TAR'], epochs_feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against TAR", fontsize=16, family='Times New Roman')
plt.xlabel("TAR (%)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\TAR against Sleep Efficiency.png", format="png") 

#%% Plot: TBR and Sleep Efficiency

plt.figure()
plt.plot(cgm_feature_df['TBR'], epochs_feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against TBR", fontsize=16, family='Times New Roman')
plt.xlabel("TBR (%)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\TBR against Sleep Efficiency.png", format="png") 

#%% Plot: max IG and Sleep Efficiency

plt.figure()
plt.plot(cgm_feature_df['max'], epochs_feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against Max BG", fontsize=16, family='Times New Roman')
plt.xlabel("Max BG (mmol/L)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)",fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\Max against Sleep Efficiency.png", format="png")   

#%% Plot: min IG and Sleep Efficiency

plt.figure()
plt.plot(cgm_feature_df['min'], epochs_feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against Min BG", fontsize=16, family='Times New Roman')
plt.xlabel("Min BG (mmol/L)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\Min against Sleep Efficiency.png", format="png")   

#%% Mean and Sleep Efficiency

plt.figure()
plt.plot(cgm_feature_df['mean'], epochs_feature_df['Efficiency'], 'o', alpha=0.5)
plt.title("Sleep Efficiency against Mean BG", fontsize=16, family='Times New Roman')
plt.xlabel("Mean BG (mmol/L)", fontsize=16, family='Times New Roman')
plt.ylabel("Sleep Efficiency (%)", fontsize=16, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()
plt.savefig(f"H:\GitHub\Bachelor\Plots\Mean against Sleep Efficiency.png", format="png") 