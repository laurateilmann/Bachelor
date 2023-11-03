# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 13:19:52 2023

@author: ltei0004
"""

import pandas as pd
from datetime import datetime
import os
import seaborn as sn
import matplotlib.pyplot as plt
import pingouin as pg

#%% Nightly correlation matrix

# Set to base directory and file path 
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data"
cgm_file = "\concatenated_cgm_51.csv"
epoch_file = "\concatenated_epochs_51.csv"

# Construct the full file paths
cgm_file_path = os.path.join(base_dir+cgm_file)
epoch_file_path = os.path.join(base_dir+epoch_file)

# Read the cgm and epoch data
cgm_data = pd.read_csv(cgm_file_path)
epoch_data = pd.read_csv(epoch_file_path)

# Merge cgm and epoch data
data = pd.merge(cgm_data, epoch_data, on=["In Bed DateTime", "Out Bed DateTime"])

# Remove duplicate id column
data = data.rename(columns={'id_y': 'id'})
data = data.drop(['id_x'], axis=1)

# Correlation matrix
corrMatrix = data.iloc[:,1:19].rcorr()

corrMatrix = pd.DataFrame(corrMatrix)


#%% Hourly correlation matrix

# Set to base directory and file path 
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data"
cgm_file = "\concatenated_hourly_cgm_11.csv"
epoch_file = "\concatenated_hourly_epochs_11.csv"

# Construct the full file paths
cgm_file_path = os.path.join(base_dir+cgm_file)
epoch_file_path = os.path.join(base_dir+epoch_file)

# Read the cgm and epoch data
cgm_data = pd.read_csv(cgm_file_path)
epoch_data = pd.read_csv(epoch_file_path)
epoch_data.replace('Bad', 0, inplace=True)
epoch_data.replace('Good', 1, inplace=True)

# Merge cgm and epoch data
data = pd.merge(cgm_data, epoch_data, on=["DateTime start"])

# Remove duplicate id column
data = data.rename(columns={'id_y': 'id'})
data = data.drop(['id_x'], axis=1)

# Correlation matrix
corrMatrix = data.iloc[:,1:14].rcorr()

#%% Old code

# # Create the correlation matrix
# corrMatrix = data.corr()


# # Plot the figure
# plt.figure()
# sn.heatmap(corrMatrix, annot=True)

# plt.get_current_fig_manager().full_screen_toggle()   

# # Save plot 
# plt.savefig("H:\GitHub\Bachelor\Plots\corrMatrixy.png", format="png")

# plt.show()


