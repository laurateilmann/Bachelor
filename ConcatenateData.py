# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 12:22:10 2023

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
import matplotlib.pyplot as plt


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
epochs_concatenate = pd.concat(dfs_epochs, ignore_index=True)

# Concatenate all the DataFrames in the list into one DataFrame
cgm_concatenate = pd.concat(dfs_cgm, ignore_index=True)      


#%% Export concatenated data to directory
epochs_output_file = os.path.join(base_dir, "concatenated_epochs.csv")

# Specify the filename for the concatenated CGM data
cgm_output_file = os.path.join(base_dir, "concatenated_cgm.csv")

# Export concatenated data to the specified files
epochs_concatenate.to_csv(epochs_output_file, index=False)
cgm_concatenate.to_csv(cgm_output_file, index=False)