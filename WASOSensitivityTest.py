# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:31:13 2023

@author: MGRO0154
"""

import os
import pandas as pd
from ActiFeaturesFunc import *
import numpy as np

#%%

def calc_WASO(data, min_consecutive_w=1):
        """
        Calculate 'wake after onset sleep' of acthigraph data 
        from in bed time to out of bed time.
    
        Parameters
        ----------
        data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W to determine sleep or wake.
    
        Returns
        -------
        Int64
        Minutes spent awake after going to sleep. Calculated for the whole night. 
    
        """
        
        # Find the index of the first 'S' occurrence
        first_s_index = data.index[data['Sleep or Awake?'] == 'S'].min()
        first_s_index -= data.index[0]
    
        # Slice the DataFrame to include rows starting from the first 'S' occurrence
        WASO_data = data.iloc[first_s_index:]
        
        # Inittialize counts and booleans 
        waso = 0 # Count of WASO each hour
        consecutive_w_count = 0 # Count of consecutive 'W's 
        new_awakening = True 
        
        for value in WASO_data['Sleep or Awake?']:
            if value == 'W':
                consecutive_w_count += 1
                if consecutive_w_count >= min_consecutive_w:
                    waso += 1
                    if new_awakening:
                        waso += 4
                        new_awakening = False
            else:
                consecutive_w_count = 0
                new_awakening = True
    
        return waso


def hourly_WASO(data,min_consecutive_w=1):
    """
    Calculate hourly 'wake after sleep onset' of acthigraph data 
        from in bed time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
    Nx2 dataframe with two columns: one with dates and times called 'DateTime',
    and one consisting of S and W to determine sleep or wake called 'Sleep or Awake?'.

    Returns
    -------
    h_WASO : list of minutes spent sleeping per hour. 

    """
        
    # Initialize lists to store hourly results
    h_WASO = []
    
    # Start and end datetime of night
    start = data.iloc[0]['DateTime']
    end = data.iloc[-1]['DateTime']
    
    # Create list of hours
    if  start.date() == end.date():
        hours = range(start.hour, end.hour+1)
    else: 
        hours = list(range(start.hour, 24)) + list(range(0, end.hour+1))
    
    # Initialize boolean. WASO_0 = True will make waso=0.
    WASO_0 = False

    # Loop through each hour of the night
    for hour in hours:
        
        # Inittialize counts and booleans 
        waso = 0 # Count of WASO each hour
        consecutive_w_count = 0 # Count of consecutive 'W's 
        preceding_w = 0 # Count of 'W's in the preceding hour 
        new_awakening = True 
       
        # Calculate the start and end times for the current hour
        start_time = hour
        end_time = hour+1 if hour<23 else 0  # Handle the transition from 23 to 0
        
        # Filter the data for the current hour
        if end_time !=0:
            mask = (data['DateTime'].dt.hour >= start_time) & (data['DateTime'].dt.hour < end_time) 
        else:
            mask = (data['DateTime'].dt.hour >= start_time)  
        data_hour = data[mask]
        
        # Check if it is the first hour of the night or if the preceding hour had WASO=0
        if hour == hours[0] or WASO_0:
            # Find the index of the first 'S' occurrence
            first_s_index = data_hour.index[data_hour['Sleep or Awake?'] == 'S'].min()
            first_s_index -= data_hour.index[0]
            # Check if there is an 'S' occurence at all
            if np.isnan(first_s_index):
                WASO_0 = True # WASO will be set to 0
            else:
                # Slice the DataFrame to include rows starting from the first 'S' occurrence
                data_hour = data_hour.iloc[first_s_index:]
                WASO_0 = False      
        
        # Count the number of 'W's in the preceding hour leading directly up to the current hour.
        # This should only be done for hours that are not the first hour of the night,
        # or hours where the preceding hours' waso=0.
        if (hour is not hours[0]) and (not WASO_0):
            # Check if the first value of the current hour is 'W'
            if data_hour.iloc[0]['Sleep or Awake?'] == 'W':
                first_index =  data_hour.index[0]
                W_present = True
                i = 1
                # While the value of the current hour is 'W' do
                while W_present:
                    # Index of the preceding value
                    preceding_index = first_index-i - data.index[0]
                    # The preceding value
                    preceding_value = data.iloc[preceding_index]['Sleep or Awake?']
                    # Check if the preceding value is 'W'
                    if preceding_value == 'W':
                        # Increment the counts by one
                        preceding_w += 1
                        consecutive_w_count += 1
                        # If the number of consecutive preceding 'W's are above
                        # or equal to min_consecutive_w, there is no need to 
                        # count further: break.
                        if preceding_w >= min_consecutive_w:
                            break
                        i += 1
                    else:
                        W_present = False
                        
        # Calculate WASO
        if not WASO_0: 
            # Iterate through the values of the current hour
            for value in data_hour['Sleep or Awake?']:
                if value == 'W':
                    # Increment the consecutive count by one
                    consecutive_w_count += 1
                    # Increment WASO by one if the consecutive count >= min_consecutive_w 
                    if consecutive_w_count >= min_consecutive_w:
                        waso += 1
                        # If it is a new awakening take into account the number
                        # of consecutive 'W's counted and increment WASO accordingly 
                        if new_awakening:
                            if preceding_w != 0:
                                waso += consecutive_w_count - preceding_w - 1
                                preceding_w = 0
                            else:
                                waso += (min_consecutive_w-1)
                            new_awakening = False
                else: # value == 'S'
                    # Reset the consecutive count
                    consecutive_w_count = 0
                    new_awakening = True
            
        # The date and start hour as pandas datetime object
        datetime_start = data.loc[data['DateTime'].dt.hour == hour, 'DateTime'].values[0] 
        datetime_start = pd.to_datetime(datetime_start)
        datetime_start = datetime_start.floor('H')
        
        # Append the hourly WASO list with the value of WASO aswell as the date and hour
        h_WASO.append([datetime_start, waso])
    
    return h_WASO

    
#%%

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = "sleep_epochs_processed.csv"
filepath = os.path.join(in_dir, filename)
epoch_data = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)

summed_filename = "summed_sleep_processed.csv"
summed_file_path = os.path.join(in_dir, summed_filename)
summed_data = pd.read_csv(summed_file_path, parse_dates=[12, 13, 14], dayfirst=True)

waso_list = []

#summed_data.shape[0]
for i in range(1):
    in_bed = summed_data.iloc[i]['In Bed DateTime']
    out_bed = summed_data.iloc[i]['Out Bed DateTime']
    
    # Extract one night's worth of actigraph epoch data
    night_data = extract_one_night(in_bed, out_bed, epoch_data)
    
    waso = hourly_WASO(night_data,5)
    waso_list.append(waso)
    


