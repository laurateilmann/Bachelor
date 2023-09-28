# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 10:26:35 2023

@author: LTEI0004


"""

#%% Import packages
import pandas as pd
import numpy as np

#%% Calculate 'Time In Range' (TIR), 'Time Above Range' (TAR) and 'Time Below Range' (TBR)

def calc_ranges(CGM_data):
    """
    Calculate 'Time In Range' (TIR), 'Time Above Range' (TAR) and 'Time Below Range' (TBR) by the definition:
    TIR: 3.9-10 mmol/L
    TAR: >10 mmol/L
    TBR: <3.9 mmol/L
    
    Parameters
    ----------
    CGM_data : Pandas Dataframe 
    Nx2 dataframe with two columns: one with dates and times called 'DateTime',
    and one with CGM data called 'CGM'.

    Returns
    -------
    list of TIR, TAR, TBR


    """
    # Define glucose concentration thresholds
    TIR_threshold_low = 3.9  # mmol/L
    TIR_threshold_high = 10.0  # mmol/L
    
    # Initialize counters for TIR, TAR, and TBR
    TIR_count = 0
    TAR_count = 0
    TBR_count = 0
    NaN_count = 0
    
    for i in range(0,len(CGM_data)):
        # Check if element is NaN
        if np.isnan(CGM_data.iloc[i]['CGM']):
            NaN_count += 1
        # Check if glucose concentration is within range
        elif (TIR_threshold_low <= CGM_data.iloc[i]['CGM']) & (CGM_data.iloc[i]['CGM'] <= TIR_threshold_high):
            TIR_count += 1
        # Check if the glucose concentration is above range
        elif CGM_data.iloc[i]['CGM'] > TIR_threshold_high:
            TAR_count += 1
        # Check if the glucose concentration is below range
        else:
            TBR_count += 1
    
    # Calculate the total number of data points
    total_data_points = len(CGM_data) - NaN_count
    
    # Calculate the percentage of data points in each range
    if total_data_points !=0:
        TIR = (TIR_count / total_data_points) * 100
        TAR = (TAR_count / total_data_points) * 100
        TBR = (TBR_count / total_data_points) * 100
    else:
        TIR = 'nan'
        TAR = 'nan'
        TBR = 'nan'
        
    return [TIR, TAR, TBR]


#%% Calculate hourly TIR, TAR and TBR
    
def hourly_ranges(CGM_data):  
    """
    Calculate hourly 'Time In Range' (TIR), 'Time Above Range' (TAR) and 'Time Below Range' (TBR) by the definition:
    TIR: 3.9-10 mmol/L
    TAR: >10 mmol/L
    TBR: <3.9 mmol/L

    Parameters
    ----------
    CGM_data : Pandas Dataframe 
    Nx2 dataframe with two columns: one with dates and times called 'DateTime',
    and one with CGM data called 'CGM'.

    Returns
    -------
    h_ranges : list of hourly TIR, TAR, TBR

    """
    
    # Initialize lists to store hourly results
    h_ranges = []
    
    # Start and end datetime of night
    start = CGM_data.iloc[0]['DateTime']
    end = CGM_data.iloc[-1]['DateTime']
    
    # Create list of hours
    if  start.date() == end.date():
        hours = range(start.hour, end.hour+1)
    else: 
        hours = list(range(start.hour, 24)) + list(range(0, end.hour+1))
  
    # Loop through each hour of the night
    for hour in hours:
        # Calculate the start and end times for the current hour
        start_time = hour
        end_time = hour+1 if hour<23 else 0  # Handle the transition from 23 to 0
        
        # Filter the data for the current hour
        if end_time !=0:
            mask = (CGM_data['DateTime'].dt.hour >= start_time) & (CGM_data['DateTime'].dt.hour < end_time) 
        else:
            mask = (CGM_data['DateTime'].dt.hour >= start_time)
            
        data_hour = CGM_data[mask]
        
        # Calculate the ranges for the current hour using your calc_ranges function
        TIR, TAR, TBR = calc_ranges(data_hour)
        
        # The date and start hour as pandas datetime object
        datetime_start = CGM_data.loc[CGM_data['DateTime'].dt.hour == hour, 'DateTime'].values[0] 
        datetime_start = pd.to_datetime(datetime_start)
        datetime_start = datetime_start.floor('H')
        
        # Append the results to the hourly lists
        h_ranges.append([datetime_start, TIR, TAR, TBR])
        
    return h_ranges
