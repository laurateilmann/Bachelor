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

def calc_awakenings(data):
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
        
        # Calculate the number of awakenings
        awakenings = ((data['Sleep or Awake?'] == 'W') & (data['Sleep or Awake?'].shift(1) == 'S'))
        num_awakenings = awakenings.sum()

        
        return num_awakenings

#%% WASO per night

def calc_WASO(data):
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
        
        # Calculate WASO
        waso = (WASO_data['Sleep or Awake?'] == 'W').sum()
        
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

def hourly_WASO(data):
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
        if WASO_0:
            WASO = 0
        else:    
            WASO = (data_hour['Sleep or Awake?'] == 'W').sum()
            
        # The date and start hour as pandas datetime object
        datetime_start = data.loc[data['DateTime'].dt.hour == hour, 'DateTime'].values[0] 
        datetime_start = pd.to_datetime(datetime_start)
        datetime_start = datetime_start.floor('H')
        
        h_WASO.append([datetime_start, WASO])
    
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
    
    criteria = {
    "Very bad sleep": {"latency": (31, np.inf), "efficiency": (0, 80), "WASO": (31, np.inf)},
    "Fairly bad sleep": {"latency": (21, 31), "efficiency": (80, 84), "WASO": (16, 30)},
    "Fairly good sleep": {"latency": (15, 20), "efficiency": (85, 90), "WASO": (5, 15)},
    "Very good sleep": {"latency": (0, 15), "efficiency": (90, 100), "WASO": (0, 5)},
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


    
    
