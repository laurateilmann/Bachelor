# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 08:33:00 2023

@author: MGRO0154
"""

#%% Import packages

import pandas as pd
from ExtractIntervals import extract_one_night
import numpy as np
import datetime

#%% Number of awakenings per night

def calc_awakenings(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculate number of awakenings of acthigraph data 
    from in bed time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
    Requires a column called 'Sleep or Awake?' consisting of S and W to determine sleep or wake. 
    
    Returns
    -------
    Int64
    Number of awakenings from in bed time to out of bed time.
    
    """
    # Find the index of the first consecutive sleep period   
    sleep_onset = calc_SO(data, min_consecutive_s)
    first_s_index = data[data['DateTime'] == sleep_onset].index[0]
    first_s_index -= data.index[0]

    # Slice the DataFrame to include rows starting from the first 'S' occurrence
    awakening_data = data.iloc[first_s_index:]
            
    # Calculate the number of awakenings
    
    consecutive_w_count = 0
    awakenings = 0
    sleep_start = False

    for value in data['Sleep or Awake?']:
        if value == 'S':
            sleep_start = True
        elif value == 'W' and sleep_start:
            consecutive_w_count += 1
            if consecutive_w_count >= min_consecutive_w:
                awakenings += 1
                consecutive_w_count = 0
                sleep_start = False
        else:
            consecutive_w_count = 0

    return awakenings

#%% WASO per night

def calc_WASO(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculate 'wake after onset sleep' of acthigraph data 
    from in bed time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
    Requires a column called 'Sleep or Awake?' consisting of S and W to determine sleep or wake.
    
    min_consecutive_w: int
    The number of minutes required to be awake before it is counted as an
    awakening and thus contributing to the WASO.

    Returns
    -------
    Int64
    Minutes spent awake after going to sleep. Calculated for the whole night. 

    """
    
    # Find the index of the first consecutive sleep period   
    sleep_onset = calc_SO(data, min_consecutive_s)
    first_s_index = data[data['DateTime'] == sleep_onset].index[0]
    first_s_index -= data.index[0]

    # Slice the DataFrame to include rows starting from the first 'S' occurrence
    WASO_data = data.iloc[first_s_index:]
    
    # Inittialize counts and booleans 
    waso = 0 # Count of WASO each hour
    consecutive_w_count = 0 # Count of consecutive 'W's 
    new_awakening = True 
    
    # Calculate WASO
    for value in WASO_data['Sleep or Awake?']:
        if value == 'W':
            consecutive_w_count += 1
            if consecutive_w_count >= min_consecutive_w:
                waso += 1
                if new_awakening:
                    waso += min_consecutive_w - 1
                    new_awakening = False
        else:
            consecutive_w_count = 0
            new_awakening = True

    return waso


#%% Average awakening length
        
def calc_avg_awakening(data):
    """
    Computes the average length of awakenings for one night.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W to 
        determine sleep or wake.

    Returns
    -------
    avg_awakening : float64
        The average length of awakening.

    """
    
    waso = calc_WASO(data)
    num_awakenings = calc_awakenings(data)
    if num_awakenings == 0:
        avg_awakening = 0
    else:
        avg_awakening = waso/num_awakenings
    
    return avg_awakening

#%% Total sleep time per night

def calc_TST(data):
    """
    Calculate 'total sleep time' of acthigraph data 
    from in bed time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
    Requires a column called 'Sleep or Awake?' consisting of S and W to determine sleep or wake.

    Returns
    -------
    Int64
    Minutes spent sleeping for the whole night. 

    """
    
    # Calculate TST
    tst = (data['Sleep or Awake?'] == 'S').sum()
    
    return tst
    
#%% Number of awakenings per hour per night
    
def hourly_awakenings(data):
    """
    Calculates number of awakenings for each hour of acthigraph data 
        from in bed time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
    Nx2 dataframe with two columns: one with dates and times called 'DateTime',
    and one consisting of S and W to determine sleep or wake called 'Sleep or Awake?'.

    Returns
    -------
    h_awakenings : list of number of awakenings per hour. 

    """
        
    # Initialize lists to store hourly results
    h_awakenings = []
    
    # Start and end datetime of night
    start = data.iloc[0]['DateTime']
    end = data.iloc[-1]['DateTime']
    
    # Create list of hours
    if  start.date() == end.date():
        hours = range(start.hour, end.hour+1)
    else: 
        hours = list(range(start.hour, 24)) + list(range(0, end.hour+1))
      
    # Loop through each hour of the night
    for hour in hours:
        
        num_awakenings = 0
        
        # Calculate the start and end times for the current hour
        start_time = hour
        end_time = hour+1 if hour<23 else 0  # Handle the transition from 23 to 0
        
        # Filter the data for the current hour
        if end_time !=0:
            mask = (data['DateTime'].dt.hour >= start_time) & (data['DateTime'].dt.hour < end_time) 
        else:
            mask = (data['DateTime'].dt.hour >= start_time)
            
        data_hour = data[mask]
    
        # Calculate the number of awakenings
        if hour is not hours[0]:
            if data_hour.iloc[0]['Sleep or Awake?'] == 'W':
                first_index =  data_hour.index[0]
                first_value = data_hour.iloc[0]['Sleep or Awake?']
                preceding_index = first_index-1 - data.index[0]
                preceding_value = data.iloc[preceding_index]['Sleep or Awake?']
                if (first_value == 'W') & (preceding_value == 'S'):
                    num_awakenings += 1
        
        awakenings = ((data_hour['Sleep or Awake?'] == 'W') & (data_hour['Sleep or Awake?'].shift(1) == 'S'))
        num_awakenings += awakenings.sum()
        
        # The date and start hour as pandas datetime object
        datetime_start = data.loc[data['DateTime'].dt.hour == hour, 'DateTime'].values[0] 
        datetime_start = pd.to_datetime(datetime_start)
        datetime_start = datetime_start.floor('H')
        
        h_awakenings.append([datetime_start, num_awakenings])
        
    return h_awakenings


#%% WASO per hour per night

def hourly_WASO(data,min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculate hourly 'wake after sleep onset' of acthigraph data 
        from in bed time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
    Nx2 dataframe with two columns: one with dates and times called 'DateTime',
    and one consisting of S and W to determine sleep or wake called 'Sleep or Awake?'.
    
    min_consecutive_w: int
    The number of minutes required to be awake before it is counted as an
    awakening and thus contributing to the WASO.

    Returns
    -------
    h_WASO : list of minutes spent sleeping per hour. 

    """
       
    # Initialize lists to store hourly results
    h_WASO = []
    
    # Start and end datetime of night
    start = data.iloc[0]['DateTime']
    end = data.iloc[-1]['DateTime']
    
    tolerance = pd.Timedelta('1 minute')
    
    # Find the sleep onset
    sleep_onset = calc_SO(data, min_consecutive_s)
    
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
            
            # Check if there is an 'S' occurence at all
            if any(abs(data_hour['DateTime']-sleep_onset)<=tolerance):
                # Find the index of the first consecutive sleep period   
                first_s_index = data_hour[data_hour['DateTime'] == sleep_onset].index[0]
                first_s_index -= data_hour.index[0]
                # Slice the DataFrame to include rows starting from the first 'S' occurrence
                data_hour = data_hour.iloc[first_s_index:]
                WASO_0 = False
            else:
                WASO_0 = True    
        
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


#%% Houly average awakening length
    
def hourly_avg_awakening(data):
    """
    Computes the average length of awakenings per hour for one night.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W to 
        determine sleep or wake.

    Returns
    -------
    avg_awakening : list
        List of average length of awakening per hour (float64). Including the 
        date and time as DateTime object. 

    """
    
    h_waso = hourly_WASO(data)
    h_awakenings = hourly_awakenings(data)
    
    # Convert the lists to NumPy arrays
    h_waso = np.array(h_waso)
    h_awakenings = np.array(h_awakenings)
    
    # Extract the timestamps (first column) and values (second column) from h_waso and h_awakenings arrays
    h_waso_timestamps = h_waso[:, 0]
    h_awakenings_timestamps = h_awakenings[:, 0]
    h_waso_values = h_waso[:, 1]
    h_awakenings_values = h_awakenings[:, 1]
    
    # Create a mask for division by zero
    division_mask = (h_awakenings_values == 0)
    
    # Perform element-wise division, setting 0 where the mask is True
    division_result = np.divide(h_waso_values, h_awakenings_values, where=~division_mask)
    
    h_avg_awakening = [[timestamp, value] for timestamp, value in zip(h_waso_timestamps, division_result)]
    
    
    return h_avg_awakening

#%% Sleep quality 
    
def calc_sleep_quality(summed_data):
    """
    Computes the sleep quality of one night. The sleep quality measure is based
    on three measurements: latency, efficiency and WASO. The criterias of these
    measurements are from: https://doi.org/10.2188/jea.JE20120012 . The 
    categories are in order from worst to best: Very bad sleep, Fairly bad sleep, 
    Fairly good sleep and Very good sleep. If just one of the criterias are met, 
    the sleep quality falls within this category. The sleep quality of the 
    person is set as the worst category obtained (e.g. if the category is 
    Fairly good sleep based on latency, but Fairly bad sleep based on WASO, 
    then the overall sleep quality is Fairly bad sleep).

    Parameters
    ----------
    summed_data : Pandas Dataframe
        1xM dataframe with at least 3 columns called "Latency", "Efficiency" 
        and "Wake After Sleep Onset (WASO)". Contains summed actigraph data
        for one person from one night. 

    Returns
    -------
    sleep_category : Str
        A category describing the sleep quality of the night. The categories are
        in order from worst to best: Very bad sleep, Fairly bad
        sleep, Fairly good sleep and Very good sleep.         
    
    """
    
    # Bad=0:
    # latency > 30
    # efficiency < 85
    # WASO > 40
    
    # Good=1 otherwise
    
    criteria = {
    0: {"latency": (31, np.inf), "efficiency": (0, 85), "WASO": (41, np.inf)},
    1: {"latency": (0, 31), "efficiency": (85, 100), "WASO": (0, 41)},
    }
    
    latency = summed_data["Latency"]
    efficiency = summed_data["Efficiency"]
    WASO = summed_data["Wake After Sleep Onset (WASO)"]
    
    # Initialize the sleep quality category as None
    sleep_category = None

    # Iterate through the defined sleep quality criteria
    for category, criteria_values in criteria.items():
        latency_range = criteria_values["latency"]
        efficiency_range = criteria_values["efficiency"]
        WASO_range = criteria_values["WASO"]
        if (
            (latency_range[0] <= latency <= latency_range[1]) or
            (efficiency_range[0] <= efficiency <= efficiency_range[1]) or
            (WASO_range[0] <= WASO <= WASO_range[1])
            ):
            sleep_category = category  # Set the sleep category if criteria are met
            break  # Exit the loop once a category is assigned
        
    return sleep_category

#%% Sleep onset 
    
def calc_SO(data, min_consecutive_s=1):
    
    sleep_onset = None
    consecutive_s_count = 0
    
    for j, value in enumerate(data['Sleep or Awake?']):
        if value == 'S':
            consecutive_s_count += 1
            if consecutive_s_count >= min_consecutive_s:
                sleep_onset = data.iloc[j - (min_consecutive_s-1)]['DateTime']
                break
        else:
            consecutive_s_count = 0
            
    return sleep_onset

#%% Calculate latency 
    
def calc_latency(data, in_bed, min_consecutive_s=1):
    
    sleep_onset = calc_SO(data, min_consecutive_s)
    
    if sleep_onset:
        latency = (sleep_onset - in_bed).total_seconds() / 60
    else:
        latency = None
    
    return latency 

    
