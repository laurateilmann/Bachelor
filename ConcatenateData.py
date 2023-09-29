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

plt.close('all')

#%% Set the base directory for the current family and session
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"

# List of families
families = ["Fam01", "Fam03", "Fam05", "Fam06", "Fam07", "Fam09"]

# List of sessions for each family
sessions = ["Baseline", "Second", "Third"]

        

#%% Initialize an empty list to store individual DataFrames
dfs_cgm = []
dfs_epochs = []


for family in families:
     for session in sessions:
         
         # Construct the file path for the CSV data for the current family and session
        cgm_path = os.path.join(base_dir, family, session, "cgm_data_processed_features.csv")
        # Construct the file path for the CSV data for the current family and session
        epoch_path = os.path.join(base_dir, family, session, "sleep_epochs_processed_features.csv")
        
         # Check if the file exists before reading it
        if os.path.exists(cgm_path) and os.path.exists(epoch_path):
            cgm_features = pd.read_csv(cgm_path, parse_dates=[0], dayfirst=True)
            epoch_features = pd.read_csv(epoch_path, parse_dates=[0], dayfirst=True)
        else:
            print(f"Either/both epoch and CGM data file does not exist in {family}/{session}. Skipping...")
            continue

        # Append the DataFrame to the list
        dfs_cgm.append(cgm_features)

        # Append the DataFrame to the list
        dfs_epochs.append(epoch_features)

# Concatenate all the DataFrames in the list into one DataFrame
epochs_feature_df = pd.concat(dfs_epochs, ignore_index=True)

# Concatenate all the DataFrames in the list into one DataFrame
cgm_feature_df = pd.concat(dfs_cgm, ignore_index=True)      
       


#%% Plot: std and WASO

plt.figure()
plt.plot(cgm_feature_df['std'], epochs_feature_df['WASO'], 'o')
plt.title("Std against WASO", fontsize=16, family='Times New Roman', fontweight='bold')
plt.xlabel("Standard deviation", fontsize=14, family='Times New Roman')
plt.ylabel("WASO (min)", fontsize=14, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()


#%% Plot: TIR and WASO

plt.figure()
plt.plot(cgm_feature_df['TIR (%)'], epochs_feature_df['WASO'], 'o')
plt.title("TIR against WASO", fontsize=16, family='Times New Roman', fontweight='bold')
plt.xlabel("Time in range (%)", fontsize=14, family='Times New Roman')
plt.ylabel("WASO (min)", fontsize=14, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()

#%% Plot: max IG and WASO

plt.figure()
plt.plot(cgm_feature_df['max'], epochs_feature_df['WASO'], 'o')
plt.title("Max IG against WASO", fontsize=16, family='Times New Roman', fontweight='bold')
plt.xlabel("Max intestinal glucose (mmol/L)", fontsize=14, family='Times New Roman')
plt.ylabel("WASO (min)",fontsize=14, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()

#%% Plot: min IG and WASO

plt.figure()
plt.plot(cgm_feature_df['min'], epochs_feature_df['WASO'], 'o')
plt.title("Min. IG against WASO", fontsize=16, family='Times New Roman', fontweight='bold')
plt.xlabel("Min. intestinal glucose (mmol/L)", fontsize=14, family='Times New Roman')
plt.ylabel("WASO (min)", fontsize=14, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()

#%% Plot: mean and TST

plt.figure()
plt.plot(cgm_feature_df['mean'], epochs_feature_df['TST'], 'o')
plt.title("Mean against TST", fontsize=16, family='Times New Roman', fontweight='bold')
plt.xlabel("Mean intestinal glucose (mmol/L)", fontsize=14, family='Times New Roman')
plt.ylabel("Total sleep time (min)", fontsize=14, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()

#%% Plot: mean and number of awakenings

plt.figure()
plt.plot(cgm_feature_df['mean'], epochs_feature_df['Number of awakenings'], 'o')
plt.title("Mean against number of awakenings", fontsize=16, family='Times New Roman', fontweight='bold')
plt.xlabel("Mean intestinal glucose (mmol/L)", fontsize=14, family='Times New Roman')
plt.ylabel("Number of awakenings", fontsize=14, family='Times New Roman')
plt.xticks(fontsize=12, family='Times New Roman')
plt.yticks(fontsize=12, family='Times New Roman')
#plt.grid()