# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:31:13 2023

@author: MGRO0154
"""

import os
import pandas as pd
from ActiFeaturesFunc import *

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
        
        consecutive_w_count = 0
        waso = 0
        
        for value in WASO_data['Sleep or Awake?']:
            if value == 'W':
                consecutive_w_count += 1
                if consecutive_w_count >= min_consecutive_w:
                    waso += 1
            else:
                consecutive_w_count = 0
    
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
    
    WASO = 0
    WASO_0 = False

    # Loop through each hour of the night
    for hour in hours:
        
        # Calculate the start and end times for the current hour
        start_time = hour
        end_time = hour+1 if hour<23 else 0  # Handle the transition from 23 to 0
        
        # Filter the data for the current hour
        if end_time !=0:
            mask = (data['DateTime'].dt.hour >= start_time) & (data['DateTime'].dt.hour < end_time) 
        else:
            mask = (data['DateTime'].dt.hour >= start_time)
            
        data_hour = data[mask]
        
        if hour == hours[0] or WASO_0:
            # Find the index of the first 'S' occurrence
            first_s_index = data_hour.index[data_hour['Sleep or Awake?'] == 'S'].min()
            first_s_index -= data_hour.index[0]
            if np.isnan(first_s_index):
                WASO_0 = True
            else:
                # Slice the DataFrame to include rows starting from the first 'S' occurrence
                data_hour = data_hour.iloc[first_s_index:]
                WASO_0 = False
        
        # Calculate WASO
        if not WASO_0:   
            consecutive_w_count = 0
            WASO = 0
            for value in data_hour['Sleep or Awake?']:
                if value == 'W':
                    consecutive_w_count += 1
                    if consecutive_w_count >= min_consecutive_w:
                        WASO += 1
                else:
                    consecutive_w_count = 0
                    
                    
        # TAG HØJDE FOR AT WASO AFHÆNGER AF FOREGÅENDE TIME
            
        # The date and start hour as pandas datetime object
        datetime_start = data.loc[data['DateTime'].dt.hour == hour, 'DateTime'].values[0] 
        datetime_start = pd.to_datetime(datetime_start)
        datetime_start = datetime_start.floor('H')
        
        h_WASO.append([datetime_start, WASO])
    
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
    
    waso = hourly_WASO(night_data)
    waso_list.append(waso)
    


