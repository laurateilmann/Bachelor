# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 13:19:52 2023

@author: ltei0004
"""

#%% Nightly correlation matrix

import pandas as pd
from datetime import datetime
import os
import seaborn as sn
import matplotlib.pyplot as plt

# Set to base directory and file path 
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM"
cgm_file = "\concatenated_cgm.csv"
epoch_file = "\concatenated_epochs.csv"

# Construct the full file paths
cgm_file_path = os.path.join(base_dir+cgm_file)
epoch_file_path = os.path.join(base_dir+epoch_file)

# Read the cgm and epoch data
cgm_data = pd.read_csv(cgm_file_path)
epoch_data = pd.read_csv(epoch_file_path)

# Merge cgm and epoch data
data = pd.merge(cgm_data, epoch_data, on=["In Bed DateTime", "Out Bed DateTime"])

data = data.rename(columns={'id_y': 'id'})
data = data.drop(['id_x'], axis=1)

# Create the correlation matrix
corrMatrix = data.corr()


# Plot the figure
plt.figure()
sn.heatmap(corrMatrix, annot=True)

plt.get_current_fig_manager().full_screen_toggle()   

# Save plot 
plt.savefig("H:\GitHub\Bachelor\Plots\corrMatrixy.png", format="png")

plt.show()

#%% Hourly correlation matrix

import pandas as pd
from datetime import datetime
import os
import seaborn as sn
import matplotlib.pyplot as plt

# Set to base directory and file path 
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"
cgm_file = "\concatenated_hourly_cgm.csv"
epoch_file = "\concatenated_hourly_epochs.csv"

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

# Create the correlation matrix
corrMatrix = data.corr()

# Plot the figure
plt.figure()
sn.heatmap(corrMatrix, annot=True)

plt.get_current_fig_manager().full_screen_toggle()   


# Save plot 
plt.savefig("H:\GitHub\Bachelor\Plots\corrMatrix_hourly.png", format="png")

plt.show()

