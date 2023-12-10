# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:05:46 2023

@author: LTEI0004 & MGRO0154

Hourly WASO plotted against various BG parameters.
"""

#%% Import packages
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

#%% Close all figures

plt.close('all')

#%% Import concatenated data

# Base directory
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data"

# File name
file = "\concatenated_hourly_all_11.csv"

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

#%% Plot: CV and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['cv'], feature_df['WASO'], 'o', label='Data Points', alpha=0.5, markersize=markersize)
plt.title("WASO against CV (hourly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("CV", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO_H against CV.png", format="png")

#%% Plot: TIR and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TIR'], feature_df['WASO'], 'o', alpha=0.5, markersize=markersize)
plt.title("WASO against TIR (hourly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("TIR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO_H against TIR.png", format="png")   

#%% Plot: TAR and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TAR'], feature_df['WASO'], 'o', alpha=0.5, markersize=markersize)
plt.title("WASO against TAR (hourly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("TAR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO_H against TAR.png", format="png") 

#%% Plot: TBR and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['TBR'], feature_df['WASO'], 'o', alpha=0.5, markersize=markersize)
plt.title("WASO against TBR (hourly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("TBR (%)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO_H against TBR.png", format="png") 

#%% Plot: max IG and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['max'], feature_df['WASO'], 'o', alpha=0.5, markersize=markersize)
plt.title("WASO against Max BG (hourly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("Max BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)",fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO_H against Max.png", format="png")   

#%% Plot: min IG and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['min'], feature_df['WASO'], 'o', alpha=0.5, markersize=markersize)
plt.title("WASO against Min BG (hourly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("Min BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO_H against Min.png", format="png")   

#%% Mean and WASO

plt.figure(figsize=(15, 10))
plt.plot(feature_df['mean'], feature_df['WASO'], 'o', alpha=0.5, markersize=markersize)
plt.title("WASO against Mean BG (hourly)", fontsize=title_size, family='Times New Roman')
plt.xlabel("Mean BG (mmol/L)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.ylabel("WASO (min)", fontsize=labelsize, family='Times New Roman', labelpad=padsize)
plt.xticks(fontsize=ticksize, family='Times New Roman')
plt.yticks(fontsize=ticksize, family='Times New Roman')
plt.tight_layout()
# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO_H against Mean.png", format="png") 


#%% Plot: CV and WASO with trend (Model_WH)

# Standardizing the data
cv_mean = feature_df['cv'].mean()
cv_std = feature_df['cv'].std()
feature_df['cv_standardized'] = (feature_df['cv'] - cv_mean) / cv_std

# Min and max used in plot
min_val_x = min(feature_df['cv_standardized'])-1
max_val_x = max(feature_df['cv_standardized'])+1
min_val_y = min(feature_df['WASO'])-5
max_val_y = max(feature_df['WASO'])+5

# Using the standardized column for the prediction
x = np.linspace(min_val_x, max_val_x, 1000)
y_pred = 9.78 + 0.61 * x # Coefficients are calculated in R

# Plotting the data
plt.figure(figsize=(15, 10))
plt.plot(feature_df['cv_standardized'], feature_df['WASO'], 'o', label='Data Points', alpha=0.5, markersize=20)
plt.plot(x, y_pred, '-', label='Prediction Line', color='red', linewidth=5)
plt.title("WASO against CV (hourly)", fontsize=45, family='Times New Roman')
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

# Save fig
plt.savefig(f"H:\GitHub\Bachelor\Plots\WASO_H vs. CV with trend.png", format="png")




