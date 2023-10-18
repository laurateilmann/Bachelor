# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:35:27 2023

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

# Choose what study to import and preprocess data from
#study = "MindYourDiabetes"
# study = "Validationstudy_2020_2021_Cecilie"
# study = "Sleep-1-child_2023_Cecilie"
#study = "Kasper" 

studies = ["MindYourDiabetes", "Sleep-1-child_2023_Cecilie", "Validationstudy_2020_2021_Cecilie"]

#%% Initialize an empty list to store individual DataFrames
dfs_cgm = []

for study in studies:
    # Base directory/path
    base_dir = os.path.join(r"L:\LovbeskyttetMapper01\StenoSleepQCGM", study)
    
    # List of families
    families = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    
    # List of sessions
    if study == "Validationstudy_2020_2021_Cecilie" or study == "Sleep-1-child_2023_Cecilie":
        sessions = [None]
    else:
        folder_path = os.path.join(base_dir,families[0])
        sessions = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
    
    
    for family in families:
         for session in sessions:
            # Create path
            if session==None:
                # Construct the file path for the CSV data for the current family and session
                cgm_path = os.path.join(base_dir, family, "cgm_data_processed.csv")

            else:
                # Construct the file path for the CSV data for the current family and session
                cgm_path = os.path.join(base_dir, family, session, "cgm_data_processed.csv")

             
            
             # Check if the file exists before reading it
            if os.path.exists(cgm_path): 
                cgm_features = pd.read_csv(cgm_path, parse_dates=[0, 1], dayfirst=True)

            else:
                print(f"CGM data file does not exist in {family}/{session}. Skipping...")
                continue
    
            # Append the DataFrame to the list
            dfs_cgm.append(cgm_features)
    

# Concatenate all the DataFrames in the list into one DataFrame
cgm_concatenate = pd.concat(dfs_cgm, ignore_index=True)    
  
# Convert 'CGM' column to numeric format
cgm_concatenate['CGM'] = pd.to_numeric(cgm_concatenate['CGM'], errors='coerce')

# Remove NaN values, if any
cgm_concatenate = cgm_concatenate.dropna(subset=['CGM'])


# Create a histogram
plt.figure(figsize=(10, 6))
plt.hist(cgm_concatenate['CGM'], bins=40, color='skyblue', edgecolor='black')

# Customize the plot
plt.title('CGM Data Histogram')
plt.xlabel('CGM Values')
plt.ylabel('Frequency')

# Show the plot
plt.show()