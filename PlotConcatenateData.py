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

cgm_file = "\concatenated_cgm.csv"
epoch_file = "\concatenated_epochs.csv"

# Construct the full file paths
cgm_file_path = os.path.join(base_dir+cgm_file)
epoch_file_path = os.path.join(base_dir+epoch_file)

# Read the cgm and epoch data
cgm_feature_df = pd.read_csv(cgm_file_path)
epochs_feature_df = pd.read_csv(epoch_file_path)

#data = pd.merge(cgm_data, epoch_data, on=["In Bed DateTime", "Out Bed DateTime"])

#%% Plot: CV and WASO

# Standardizing the data
cv_mean = cgm_feature_df['cv'].mean()
cv_std = cgm_feature_df['cv'].std()
cgm_feature_df['cv_standardized'] = (cgm_feature_df['cv'] - cv_mean) / cv_std

# Using the standardized column for the prediction
x = np.linspace(min(cgm_feature_df['cv_standardized']), max(cgm_feature_df['cv_standardized']), 1000)
y_pred = 88.627 + 7.525 * x

# Plotting the data
plt.figure()
plt.plot(cgm_feature_df['cv_standardized'], epochs_feature_df['WASO'], 'o', label='Data Points')
plt.plot(x, y_pred, '-', label='Prediction Line', color='red', linewidth=2)
plt.title("CV against WASO$_{1min}$", fontsize=16, family='Times New Roman', fontweight='bold')
plt.xlabel("Coefficient of variation", fontsize=14, family='Times New Roman')
plt.ylabel("WASO (min)", fontsize=14, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
legend_font = {'family': 'Times New Roman', 'size': 12}
plt.legend(prop=legend_font)
plt.show()

plt.savefig(f"H:\GitHub\Bachelor\Plots\CV vs. WASO11.png", format="png")

#%%

# #%% Plot: TIR and WASO

# plt.figure()
# plt.plot(cgm_feature_df['TIR'], epochs_feature_df['WASO'], 'o')
# plt.title("TIR against WASO", fontsize=16, family='Times New Roman', fontweight='bold')
# plt.xlabel("Time in range (%)", fontsize=14, family='Times New Roman')
# plt.ylabel("WASO (min)", fontsize=14, family='Times New Roman')
# plt.xticks(fontsize=12, family='Times New Roman')
# plt.yticks(fontsize=12, family='Times New Roman')
# #plt.grid()

# #%% Plot: max IG and WASO

# plt.figure()
# plt.plot(cgm_feature_df['max'], epochs_feature_df['WASO'], 'o')
# plt.title("Max IG against WASO", fontsize=16, family='Times New Roman', fontweight='bold')
# plt.xlabel("Max intestinal glucose (mmol/L)", fontsize=14, family='Times New Roman')
# plt.ylabel("WASO (min)",fontsize=14, family='Times New Roman')
# plt.xticks(fontsize=12, family='Times New Roman')
# plt.yticks(fontsize=12, family='Times New Roman')
# #plt.grid()

# #%% Plot: min IG and WASO

# plt.figure()
# plt.plot(cgm_feature_df['min'], epochs_feature_df['WASO'], 'o')
# plt.title("Min. IG against WASO", fontsize=16, family='Times New Roman', fontweight='bold')
# plt.xlabel("Min. intestinal glucose (mmol/L)", fontsize=14, family='Times New Roman')
# plt.ylabel("WASO (min)", fontsize=14, family='Times New Roman')
# plt.xticks(fontsize=12, family='Times New Roman')
# plt.yticks(fontsize=12, family='Times New Roman')
# #plt.grid()

# #%% Plot: mean and TST

# plt.figure()
# plt.plot(cgm_feature_df['mean'], epochs_feature_df['TST'], 'o')
# plt.title("Mean against TST", fontsize=16, family='Times New Roman', fontweight='bold')
# plt.xlabel("Mean intestinal glucose (mmol/L)", fontsize=14, family='Times New Roman')
# plt.ylabel("Total sleep time (min)", fontsize=14, family='Times New Roman')
# plt.xticks(fontsize=12, family='Times New Roman')
# plt.yticks(fontsize=12, family='Times New Roman')
# #plt.grid()

# #%% Plot: mean and number of awakenings

# plt.figure()
# plt.plot(cgm_feature_df['mean'], epochs_feature_df['Number of awakenings'], 'o')
# plt.title("Mean against number of awakenings", fontsize=16, family='Times New Roman', fontweight='bold')
# plt.xlabel("Mean intestinal glucose (mmol/L)", fontsize=14, family='Times New Roman')
# plt.ylabel("Number of awakenings", fontsize=14, family='Times New Roman')
# plt.xticks(fontsize=12, family='Times New Roman')
# plt.yticks(fontsize=12, family='Times New Roman')
# #plt.grid()

# #%% Plot: Logaritmh TAR against WASO

# plt.figure()
# plt.plot(np.log(cgm_feature_df['TAR']), (epochs_feature_df['WASO']), 'o')
# plt.title("Logarithm of TAR against Logarithm of WASO", fontsize=16)
# plt.xlabel("Logarithm of Time Above range (%)", fontsize=14)
# plt.ylabel("WASO (min)", fontsize=14)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)

# plt.show()


# #%% Pairwise scatterplot

# plt.close('all')

# cgm_features_plot = cgm_feature_df.iloc[:,2:]
# epoch_features_plot = epochs_feature_df.iloc[:,2:]

# all_features = pd.concat([cgm_features_plot,epoch_features_plot],axis=1)

# for i, cgm_feature in enumerate(cgm_features_plot):
    
#     # Create subplots for each CGM feature
#     fig, axes = plt.subplots(2, 4, figsize=(17, 10))
    
#     for j, epoch_feature in enumerate(epoch_features_plot):
#         ax = axes[j//4, j%4]
#         ax.scatter(cgm_features_plot[cgm_feature], epoch_features_plot[epoch_feature])
#         ax.set_xlabel(cgm_feature, fontsize=20)
#         ax.set_ylabel(epoch_feature, fontsize=20)
#         ax.tick_params(axis='x', labelsize=20)
#         ax.tick_params(axis='y', labelsize=20) 

#     # Remove excess axes 
#     axes[1, 3].set_axis_off() 
    
#     plt.tight_layout()
#     plt.show()
    
#     # Save plot 
#     plt.savefig(f"H:\GitHub\Bachelor\Plots\{cgm_feature} vs. sleep features.png", format="png")   
    
#%% 
    
plt.figure()
plt.plot(cgm_feature_df['std'], epochs_feature_df['WASO'], 'o')
plt.title("Standard deviation against WASO", fontsize=16)
plt.xlabel("Std of IG (mmol/L)", fontsize=14)
plt.ylabel("WASO", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Save plot 
plt.savefig(f"H:\GitHub\Bachelor\Plots\Standard deviation against WASO.png", format="png")   

plt.figure()
plt.plot(cgm_feature_df['cv'], epochs_feature_df['WASO'], 'o')
plt.title("Coefficient of variation against WASO", fontsize=16)
plt.xlabel("CV of IG", fontsize=14)
plt.ylabel("WASO", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Save plot 
plt.savefig(f"H:\GitHub\Bachelor\Plots\Coefficient of variation against WASO.png", format="png")   

plt.figure()
plt.plot(cgm_feature_df['delta IG'], epochs_feature_df['WASO'], 'o')
plt.title("Delta IG against WASO", fontsize=16)
plt.xlabel("Delta IG of IG (mmol/L)", fontsize=14)
plt.ylabel("WASO", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Save plot 
plt.savefig(f"H:\GitHub\Bachelor\Plots\Delta IG against WASO.png", format="png")   



    