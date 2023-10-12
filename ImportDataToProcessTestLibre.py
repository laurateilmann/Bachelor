# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 12:37:59 2023

@author: LTEI0004


A program to import Actigraph data in agd format, CGM data and the summed actigraph data in csv format and finally export 
to L-drev. 

"""

#%% Import packages

import os
import pyActigraphy
import plotly.io as io
import pandas as pd
from datetime import datetime 
from MarkMissingData import MarkMissingData
from CalcPctActiveTime import *
import csv

#%% 

# Set the base directory where files are located
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"

# List of families
families = ["Fam05"]

# List of sessions for each family
sessions = ["Baseline"]

# Settings for figures
io.renderers.default = 'browser'  # Set to 'svg' to open in Spyder plot tab

#%% Import all CGM data and export processed file
            
# Loop through each family
for family in families:
    # Loop through each session for the family
    for session in sessions:
        cgm_dir = os.path.join(base_dir, family, session)

        # List all CGM files (assuming they are all CSV files named "cgm_data.csv") in the current session
        cgm_files = [file for file in os.listdir(cgm_dir) if file in ["cgm_data.csv", "cgm_data_clarity.csv", "cgm_data_libre.csv"]]

        # Loop through each CGM file in the session and process it
        for filename in cgm_files:
            if filename == "cgm_data.csv":
                # Import CGM data
                cgm_data = pd.read_csv(os.path.join(cgm_dir, filename),skiprows=2, parse_dates = [0], 
                          dayfirst=True, usecols = [0,1], names = ['DateTime','CGM'])
                
            elif filename == "cgm_data_clarity.csv":
                # Import CGM data
                cgm_data = pd.read_csv(os.path.join(cgm_dir, filename),skiprows=12, parse_dates = [0], 
                          dayfirst=True, delimiter=';', usecols = [1,7], names = ['DateTime','CGM'])
                
                # Create a temporary dataframe where 'Lav' and 'Høj' are changed to None 
                cgm_data_temp = cgm_data['CGM'].replace({'Lav':None, 'Høj':None})
                # Change temp CGM values to float
                cgm_data_temp = cgm_data_temp.astype(float)
                # Find min and max
                min_val = str(cgm_data_temp.min())
                max_val = str(cgm_data_temp.max())
                # Replace 'Lav' and 'Høj' with min and max, repsectively, in original CGM data. 
                cgm_data['CGM'] = cgm_data['CGM'].replace({'Lav':min_val, 'Høj':max_val})
                # Change CGM values to float
                cgm_data['CGM'] = cgm_data['CGM'].astype(float)
                
            # else:
            #     # Import CGM data
            #     cgm_data = pd.read_csv(os.path.join(cgm_dir, filename), parse_dates = [0], 
            #               dayfirst=True, delimiter=';', usecols = [0,1], names = ['DateTime','CGM'])
                
            #     # Remove all rows where 'DateTime' is 'NaT'
            #     cgm_data = cgm_data[cgm_data['DateTime'].notna()]
            #     # Replace '.' in 'CGM' with NaN
            #     cgm_data['CGM'] = cgm_data['CGM'].replace({'.':float("nan")})
            #     # Convert CGM values to float
            #     cgm_data['CGM'] = cgm_data['CGM'].astype(float)
                
            # Sort by date and time
            cgm_data.sort_values(by = 'DateTime', inplace = True)
            # Reset index, so first row is index 0
            cgm_data = cgm_data.reset_index(drop = True)
            # Find holes in data where data is missing and insert NaN
            cgm_data = MarkMissingData(cgm_data)
            
            # Filter away any blood glucose values above 40 mmol/L (artefacts)
            for i in range(0,len(cgm_data)):
                if cgm_data.loc[i,'CGM'] > 40:
                    cgm_data.loc[i,'CGM'] = float("nan") 
                    
            # Percent active CGM time. OBS: not used or exported at the moment
            PctActiveTime, TotalTime = CalcPctActiveTime(cgm_data)
            
            # Export processed CGM data
            processed_filename = "cgm_data_processed.csv"
            output_path = os.path.join(cgm_dir, processed_filename)
            cgm_data.to_csv(output_path, index=False)
            
            print(f"Processed {filename} and saved as {processed_filename} in {family}/{session}")