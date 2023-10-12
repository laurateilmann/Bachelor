# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 12:41:28 2023

@author: MGRO0154
"""


import os
import pyActigraphy
import plotly.io as io
import pandas as pd
from datetime import datetime 
from MarkMissingData import MarkMissingData
from CalcPctActiveTime import *

#%% 

# Set the base directory where files are located
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Validationstudy_2020_2021_Cecilie"

# List of families
families = ["PAT9"]

family = "PAT9"

#%% Import all CGM data and export processed file
            
# Loop through each family
for family in families:
   
    cgm_dir = os.path.join(base_dir, family)

    # List all CGM files (assuming they are all CSV files named "cgm_data.csv") in the current session
    cgm_files = [file for file in os.listdir(cgm_dir) if file in ["svendsen nanna 11-09-2023.csv"]]

    # Loop through each CGM file in the session and process it
    for filename in cgm_files:
        # Import CGM data
        cgm_data = pd.read_csv(
            os.path.join(cgm_dir, filename), 
            delimiter=";",
            skiprows=7,
            usecols = [1,2,32], names = ['Date', 'Time' ,'CGM'],
            parse_dates = [0,1], dayfirst=True,
            low_memory=False)
        
        # Find the index just before the CGM values start
        first_index = cgm_data[cgm_data['CGM'] == "Sensor Glucose (mmol/L)"].index[0]
        # Use only the rows where the CGM values are
        cgm_data = cgm_data.iloc[first_index+1:]
        
        # Convert dates and times to datetime
        cgm_data['Date'] = pd.to_datetime(cgm_data['Date'])
        cgm_data['Time'] = pd.to_datetime(cgm_data['Time']).dt.time
        # Combine dates with times
        cgm_data['DateTime'] = cgm_data.apply(lambda x: datetime.combine(x['Date'], x['Time']), axis=1) 
        # Remove old Date and Time columns
        cgm_data = cgm_data.drop(['Date', 'Time'], axis=1)
        
        # Remove all rows where DateTime is 00:00:00 (H:M:S) regardless of what the date is
        mask = cgm_data['DateTime'].dt.strftime('%H:%M:%S') != '00:00:00'
        cgm_data = cgm_data[mask]
        # Remove seconds 
        cgm_data['DateTime'] =cgm_data['DateTime'].dt.floor('T')

        # Replace commas with periods
        cgm_data = cgm_data.replace(',','.',regex=True)
        # Make CGM values float64
        cgm_data['CGM'] = pd.to_numeric(cgm_data['CGM'], errors='coerce')
        
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
        # processed_filename = "cgm_data_processed.csv"
        # output_path = os.path.join(cgm_dir, processed_filename)
        # cgm_data.to_csv(output_path, index=False)
        
        # print(f"Processed {filename} and saved as {processed_filename} in {family}/{session}")