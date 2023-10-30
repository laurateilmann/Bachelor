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

# Choose what studies to concatenate
studies = ["MindYourDiabetes", "Sleep-1-child_2023_Cecilie", "Validationstudy_2020_2021_Cecilie"]
# studies = ["MindYourDiabetes"]
# studies = ["Sleep-1-child_2023_Cecilie"]
# studies = ["Validationstudy_2020_2021_Cecilie"]

base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM"

#%% Initialize an empty list to store individual DataFrames
dfs_cgm = []
dfs_epochs = []

for study in studies:
    # Base directory/path
    study_dir = os.path.join(base_dir, study)
    
    # List of families
    families = [folder for folder in os.listdir(study_dir) if os.path.isdir(os.path.join(study_dir, folder))]
    
    # List of sessions
    if study == "Validationstudy_2020_2021_Cecilie" or study == "Sleep-1-child_2023_Cecilie":
        sessions = [None]
    else:
        folder_path = os.path.join(study_dir,families[0])
        sessions = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
    
    
    for family in families:
         for session in sessions:
            # Create path
            if session==None:
                # Construct the file path for the CSV data for the current family and session
                cgm_path = os.path.join(study_dir, family, "cgm_data_processed_features.csv")
                # Construct the file path for the CSV data for the current family and session
                epoch_path = os.path.join(study_dir, family, "sleep_epochs_processed_features.csv")
            else:
                # Construct the file path for the CSV data for the current family and session
                cgm_path = os.path.join(study_dir, family, session, "cgm_data_processed_features.csv")
                # Construct the file path for the CSV data for the current family and session
                epoch_path = os.path.join(study_dir, family, session, "sleep_epochs_processed_features.csv")
             
            
             # Check if the file exists before reading it
            if os.path.exists(cgm_path) and os.path.exists(epoch_path):
                cgm_features = pd.read_csv(cgm_path, parse_dates=[0, 1], dayfirst=True)
                epoch_features = pd.read_csv(epoch_path, parse_dates=[0, 1], dayfirst=True)
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

# Merge the two dataframes based on index
merged_data = cgm_concatenate.merge(epochs_concatenate, left_index=True, right_index=True, how='inner')

# Rename DateTime and id columns
merged_data = merged_data.rename(columns={'In Bed DateTime_x': 'In Bed DateTime', 'Out Bed DateTime_x': 'Out Bed DateTime', 'id_y': 'id'})

# Remove duplicate DateTime and id columns
merged_data = merged_data.drop(['In Bed DateTime_y', 'Out Bed DateTime_y', 'id_x'], axis=1)


#%% Export concatenated data to directory

if len(studies)==1:
    output_dir = study_dir 
else:
    output_dir = base_dir

# Specify the filename for the concatenated sleep epoch and CGM data
epochs_output_file = os.path.join(output_dir, "concatenated_epochs.csv")
cgm_output_file = os.path.join(output_dir, "concatenated_cgm.csv")
merged_output_file = os.path.join(output_dir, "concatenated_all.csv")

# Export concatenated data to the specified files
epochs_concatenate.to_csv(epochs_output_file, index=False)
cgm_concatenate.to_csv(cgm_output_file, index=False)
merged_data.to_csv(merged_output_file, index=False)