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
from PrepareLibreviewData import *
import numpy as np

#%% 

# Choose what study to import and preprocess data from
# study = "MindYourDiabetes"
# study = "Validationstudy_2020_2021_Cecilie"
study = "Sleep-1-child_2023_Cecilie"
# study = "Kasper" 

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
    

#%% Import all AGD files and export processed file as csv

# Loop through each family
for family in families:
    # Loop through each session for the family
    for session in sessions:
        # Create path
        if session==None:
            in_dir = os.path.join(base_dir, family)
        else:
            in_dir = os.path.join(base_dir, family, session)


        # List all AGD files in the current session
        agd_files = [file for file in os.listdir(in_dir) if file.endswith(".agd")]

        # Loop through each AGD file in the session and process it
        for filename in agd_files:
            # Import agd file
            raw = pyActigraphy.io.read_raw_agd(os.path.join(in_dir, filename))
            
            # Extract vector magnitude and timestamps from pyActigraphy dataframe
            timestamps = pd.to_datetime(raw.data.index)
            data = pd.DataFrame({'DateTime': timestamps, 'Magnitude': raw.data}) 
            data = data.reset_index(drop=True)
            
            # Export dataframe
            processed_filename = os.path.splitext(filename)[0] + '_processed.csv'
            output_dir = in_dir
            output_path = os.path.join(output_dir, processed_filename)
            data.to_csv(output_path, index=False)
            
            print(f"Processed {filename} and saved as {processed_filename} in {family}/{session}")



#%% Import all CGM data and export processed file
            
# Loop through each family
for family in families:
    # Loop through each session for the family
    for session in sessions:
        # Create path
        if session==None:
            cgm_dir = os.path.join(base_dir, family)
        else:
            cgm_dir = os.path.join(base_dir, family, session)

        # List all CGM files (assuming they are all CSV files named "cgm_data.csv") in the current session
        cgm_files = [file for file in os.listdir(cgm_dir) if file in ["cgm_data.csv", 
                                                                      "cgm_data_clarity.csv", 
                                                                      "cgm_data_guardian.csv", 
                                                                      "cgm_data_libre.csv",
                                                                      "cgm_data_xls.xls",
                                                                      "cgm_data_switched.csv"]]

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
            elif filename == "cgm_data_guardian.csv":
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
                
                # Replace / with - in dates to make further processing possible
                cgm_data = cgm_data.replace('/','-',regex=True)
                # Possbile date formats
                date_formats = ['%d-%m-%Y', '%Y-%m-%d']
                # Try the different date formats
                for date_format in date_formats:
                    try:
                        # Convert dates to datetime
                        cgm_data['Date'] = pd.to_datetime(cgm_data['Date'], format=date_format)               
                        break  # Exit the loop if successful parsing
                    except ValueError:
                        continue
                
                # Convert times to datetime
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
                # Reorder columns
                cgm_data = cgm_data[['DateTime', 'CGM']]
            elif filename == "cgm_data_libre.csv":
                cgm_data = PrepareLibreviewData(os.path.join(cgm_dir, filename))
            elif filename == "cgm_data_xls.xls":
                cgm_data = pd.read_excel(os.path.join(cgm_dir, filename), sheet_name='CGM', 
                                          skiprows=4, parse_dates = [0], usecols = [0,1], names = ['DateTime','CGM'])
            else:
                # Import CGM data
                cgm_data = pd.read_csv(os.path.join(cgm_dir, filename),skiprows=2, parse_dates = [1], 
                          dayfirst=True, usecols = [0,1], names = ['CGM','DateTime'])
                # Floor seconds and remove UTC offset
                cgm_data['DateTime'] =cgm_data['DateTime'].dt.floor('T')
                cgm_data['DateTime'] =cgm_data['DateTime'].dt.tz_localize(None)
                # Reorder columns
                cgm_data = cgm_data[['DateTime', 'CGM']]

            if filename != "cgm_data_libre.csv":
                # Sort by date and time
                cgm_data.sort_values(by = 'DateTime', inplace = True)
                # Reset index, so first row is index 0
                cgm_data = cgm_data.reset_index(drop = True)
                # Find holes in data where data is missing and insert NaN
                cgm_data = MarkMissingData(cgm_data)
            
            # Replace values of 111.1 mmol/L with NaN, since these are a systemic error
            cgm_data['CGM'] = cgm_data['CGM'].replace(111.1, np.nan)

            # Filter away any blood glucose values above 40 mmol/L (artefacts)
            cgm_data['CGM'] = cgm_data['CGM'].where(cgm_data['CGM'] < 40, np.nan)
                    
            # Percent active CGM time. OBS: not used or exported at the moment
            PctActiveTime, TotalTime = CalcPctActiveTime(cgm_data)
            
            # Export processed CGM data
            processed_filename = "cgm_data_processed.csv"
            output_path = os.path.join(cgm_dir, processed_filename)
            cgm_data.to_csv(output_path, index=False)
            
            print(f"Processed {filename} and saved as {processed_filename} in {family}/{session}")

#%% Import summed actigraph data and export processed file
            
# Loop through each family
for family in families:
    # Loop through each session for the family
    for session in sessions:
        # Create path
        if session==None:
            summed_data_dir = os.path.join(base_dir, family)
        else:
            summed_data_dir = os.path.join(base_dir, family, session)

        # List all summed data files (assuming they are all CSV files with the same naming convention)
        summed_data_files = [file for file in os.listdir(summed_data_dir) if file == "summed_sleep.csv"]

        # Loop through each summed data file in the session and process it
        for filename in summed_data_files:
            # Import summed data
            summed_data = pd.read_csv(os.path.join(summed_data_dir, filename), skiprows=5, encoding='cp850')

            # Convert dates and times to datetime
            summed_data['In Bed Date'] = pd.to_datetime(summed_data['In Bed Date'],format='%d-%m-%Y')
            summed_data['In Bed Time'] = pd.to_datetime(summed_data['In Bed Time']).dt.time
            summed_data['Out Bed Date'] = pd.to_datetime(summed_data['Out Bed Date'],format='%d-%m-%Y')
            summed_data['Out Bed Time'] = pd.to_datetime(summed_data['Out Bed Time']).dt.time
            summed_data['Onset Date'] = pd.to_datetime(summed_data['Onset Date'],format='%d-%m-%Y')
            summed_data['Onset Time'] = pd.to_datetime(summed_data['Onset Time']).dt.time

            # Combine dates with times
            summed_data['In Bed DateTime'] = summed_data.apply(lambda x: datetime.combine(x['In Bed Date'], x['In Bed Time']), axis=1) 
            summed_data['Out Bed DateTime'] = summed_data.apply(lambda x: datetime.combine(x['Out Bed Date'], x['Out Bed Time']), axis=1) 
            summed_data['Onset DateTime'] = summed_data.apply(lambda x: datetime.combine(x['Onset Date'], x['Onset Time']), axis=1) 

            # Remove old Date and Time columns
            summed_data = summed_data.drop(['In Bed Date', 'In Bed Time','Out Bed Date', 'Out Bed Time','Onset Date','Onset Time'], axis=1)

            # Replace commas with periods
            summed_data = summed_data.replace(',','.',regex=True)

            # Export processed summed data
            processed_filename = os.path.splitext(filename)[0] + '_processed.csv'
            output_dir = summed_data_dir
            output_path = os.path.join(output_dir, processed_filename)
            summed_data.to_csv(output_path, index=False)
            
            print(f"Processed {filename} and saved as {processed_filename} in {family}/{session}")
            
#%% Import epoch actigraph data and export processed file
            
for family in families:
    for session in sessions:
        # Create path
        if session==None:
            epoch_dir = os.path.join(base_dir, family)
        else:
            epoch_dir = os.path.join(base_dir, family, session)
        
        # Define the path to the file to be checked
        filename = "sleep_epochs"
        file_path = os.path.join(epoch_dir, filename + '.csv')

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f" Sleep epochs file does not exist in {family}/{session}. Skipping...")
            continue  # Skip to the next iteration if the file does not exist

        # Import actigraphy data
        df = pd.read_csv(file_path, skiprows=4, encoding='cp850')

        # Convert columns into actual columns and not index-columns
        df = df.reset_index()
        # Remove column called 'index'
        df = df.drop('index', axis=1)

        # Remove rows introducing each sleep period/night
        values_to_remove = ['Sleep Period', 'Date']
        mask = ~df['Date'].isin(values_to_remove)
        df = df[mask]

        # Convert Date and Time columns to Datetime format and combine them
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        df['Time'] = pd.to_datetime(df['Time']).dt.time
        df['DateTime'] = df.apply(lambda x: datetime.combine(x['Date'], x['Time']), axis=1)
        # Remove old Date and Time columns
        df = df.drop(['Date', 'Time'], axis=1)

        # Sort by date and time
        df.sort_values(by='DateTime', inplace=True)
        # Reset index, so the first row is index 0
        df = df.reset_index(drop=True)

        # Keep only 'DateTime' and 'Sleep or Awake?' columns
        columns_to_keep = ['DateTime', 'Sleep or Awake?']
        df = df[columns_to_keep]
        
        
        # Export processed epoch data
        processed_filename = os.path.splitext(filename)[0] + '_processed.csv'
        output_path = os.path.join(epoch_dir, processed_filename)
        df.to_csv(output_path, index=False)
          
        print(f"Processed {filename} and saved as {processed_filename} in {family}/{session}")


