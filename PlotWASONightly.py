# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:05:46 2023

@author: ltei0004
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

file = "\concatenated_all_11.csv"

# Construct the full file paths
file_path = os.path.join(base_dir+file)

# Read the cgm and epoch data
feature_df = pd.read_csv(file_path)

#%% Plotting settings

markersize = 20
title_size = 55
labelsize = 50
ticksize = 45
padsize = 20

#%% Plot: CV and WASO with trend

# Standardizing the data
cv_mean = feature_df['cv'].mean()
cv_std = feature_df['cv'].std()
feature_df['cv_standardized'] = (feature_df['cv'] - cv_mean) / cv_std

# Min and max used in plot
min_val_x = min(feature_df['cv_standardized'])-0.5
max_val_x = max(feature_df['cv_standardized'])+0.5
min_val_y = min(feature_df['WASO'])-15
max_val_y = max(feature_df['WASO'])+35

# Using the standardized column for the prediction
x = np.linspace(min_val_x, max_val_x, 1000)
y_pred = 88.627 + 7.525 * x # Coefficients are calculated in R

# Plotting the data
plt.figure(figsize=(15, 10))
plt.plot(feature_df['cv_standardized'], feature_df['WASO'], 'o', label='Data Points', alpha=0.5, markersize=20)
plt.plot(x, y_pred, '-', label='Prediction Line', color='red', linewidth=5)
plt.title("WASO against CV (nightly)", fontsize=45, family='Times New Roman')
plt.xlabel("CV", fontsize=42, family='Times New Roman', labelpad=20)
plt.ylabel("WASO (min)", fontsize=42, family='Times New Roman', labelpad=20)
plt.xticks(fontsize=40, family='Times New Roman')
plt.yticks(fontsize=40, family='Times New Roman')
legend_font = {'family': 'Times New Roman', 'size': 40}
plt.legend(prop=legend_font)
plt.xlim(min_val_x, max_val_x)
plt.ylim(min_val_y, max_val_y)
plt.tight_layout()
plt.show()

plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO vs. CV with trend.png", format="png")

#%% Plot: CV and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['cv'], feature_df['WASO'], 'o', label='Data Points', alpha=0.5, markersize=markersize)
plt.title("WASO against CV (nightly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("CV", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO against CV.png", format="png")


#%% Plot: TIR and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TIR'], feature_df['WASO'], 'o', alpha=0.5, markersize=20)
plt.title("WASO against TIR (nightly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("TIR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO against TIR.png", format="png")   

#%% Plot: TAR and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TAR'], feature_df['WASO'], 'o', alpha=0.5, markersize=20)
plt.title("WASO against TAR (nightly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("TAR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO against TAR.png", format="png") 

#%% Plot: TBR and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TBR'], feature_df['WASO'], 'o', alpha=0.5, markersize=20)
plt.title("WASO against TBR (nightly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("TBR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO against TBR.png", format="png") 

#%% Plot: Max BG and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['max'], feature_df['WASO'], 'o', alpha=0.5, markersize=20)
plt.title("WASO against Max BG (nightly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("Max BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)",fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO against Max.png", format="png")   

#%% Plot: Min BG and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['min'], feature_df['WASO'], 'o', alpha=0.5, markersize=20)
plt.title("WASO against Min BG (nightly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("Min BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO against Min.png", format="png")   

#%% Plot: Mean BG and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['mean'], feature_df['WASO'], 'o', alpha=0.5, markersize=20)
plt.title("WASO against Mean BG (nightly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("Mean BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO against Mean.png", format="png") 


#%% Plot: Logaritmh TAR against WASO

# plt.figure()
# plt.plot(np.log(feature_df['TAR']), (feature_df['WASO']), 'o')
# plt.title("LogTAR against WASO", fontsize=16)
# plt.xlabel("Logarithm of Time above range (%)", fontsize=16)
# plt.ylabel("WASO (min)", fontsize=16)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.show()

# #%% Plot: Logaritmh TIR against WASO

# plt.figure()
# plt.plot(np.log(feature_df['TIR']), (feature_df['WASO']), 'o')
# plt.title("LogTIR against WASO", fontsize=16)
# plt.xlabel("Logarithm of Time in range (%)", fontsize=16)
# plt.ylabel("WASO (min)", fontsize=16)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.show()


# #%% Plot: Logaritmh TBR against WASO

# plt.figure()
# plt.plot(np.log(feature_df['TBR']), (feature_df['WASO']), 'o')
# plt.title("LogTBR against WASO", fontsize=16)
# plt.xlabel("Logarithm of Time below range (%)", fontsize=16)
# plt.ylabel("WASO (min)", fontsize=16)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.show()






    