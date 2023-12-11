# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 08:33:00 2023

@author: MGRO0154 & LTEI0004

Functions for computing sleep parameters/features. 
"""

#%% Import packages

import pandas as pd
import numpy as np
import datetime

#%% Number of awakenings per night

def calc_awakenings(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculate number of awakenings of acthigraph data from in bed time to out 
    of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
    
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 
    
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
            
    # Initilize counts and booleans
    consecutive_w_count = 0
    awakenings = 0
    new_awakening = True

    # Calculate the number of awakenings
    for value in awakening_data['Sleep or Awake?']:
        if value == 'W' and new_awakening:
            # Increment the consecutive count by one
            consecutive_w_count += 1
            # Increment num_awakenings by one if the consecutive count >= min_consecutive_w 
            if consecutive_w_count >= min_consecutive_w:
                awakenings += 1
                new_awakening = False
        elif value == 'S':
            consecutive_w_count = 0
            new_awakening = True
    
    return awakenings

#%% WASO per night

def calc_WASO(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculate 'wake after onset sleep' (WASO) of acthigraph data from in bed 
    time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
    
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute.  

    Returns
    -------
    Int64
        Minutes spent awake after going to sleep. Calculated for the whole night
        from In Bed to Out Bed. 

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
        
def calc_avg_awakening(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Computes the average length of awakenings for one night.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
        
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 

    Returns
    -------
    avg_awakening : float64
        The average length of awakening in minutes.

    """
    
    waso = calc_WASO(data, min_consecutive_w, min_consecutive_s)
    num_awakenings = calc_awakenings(data, min_consecutive_w, min_consecutive_s)
    if num_awakenings == 0:
        avg_awakening = 0
    else:
        avg_awakening = waso/num_awakenings
    
    return avg_awakening

#%% Total sleep time per night

def calc_TST(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculate 'total sleep time' (TST) of acthigraph data from in bed time to 
    out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
        
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 

    Returns
    -------
    Int64
        Minutes spent sleeping for the whole night from In Bed to Out Bed. 

    """
    # Calculate WASO (number of minutes awake after sleep onset)
    waso = calc_WASO(data, min_consecutive_w, min_consecutive_s)
    
    # Find sleep onset
    sleep_onset = calc_SO(data, min_consecutive_s)
    
    # Slice data to after sleep onset
    sleep_onset_index = data[data['DateTime'] == sleep_onset].index[0]
    sleep_onset_index -= data.index[0]
    data_tst = data.iloc[sleep_onset_index:]

    # Calculate TST
    tst = data_tst.shape[0] - waso
    
    return tst
    
#%% Number of awakenings per hour per night
    
def hourly_awakenings(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculates number of awakenings for each hour of acthigraph data from in
    bed time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
        
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 

    Returns
    -------
    h_awakenings : list of number of awakenings per hour. 

    """
        
    # Initialize lists to store hourly results
    h_awakenings = []
    
    # Find the sleep onset
    sleep_onset = calc_SO(data, min_consecutive_s)
    
    # Tolerance for comparing timestamps to sleep onset (in seconds)
    tolerance = pd.Timedelta('1 minute').total_seconds()
    
    # Start and end datetime of night
    start = data.iloc[0]['DateTime']
    end = data.iloc[-1]['DateTime']
    
    # Create list of hours
    if  start.date() == end.date():
        hours = range(start.hour, end.hour+1)
    else: 
        hours = list(range(start.hour, 24)) + list(range(0, end.hour+1))
    
    # Initialise booleans
    sleep_onset_occured = False
    new_awakening = True
    
    # Loop through each hour of the night
    for hour in hours:
        
        # Inittialize counts and booleans 
        num_awakenings = 0 # Count of awakenings each hour
        consecutive_w_count = 0 # Count of consecutive 'W's 
        subsequent_w = True
        
        # Calculate the start and end times for the current hour
        start_time = hour
        end_time = hour+1 if hour<23 else 0  # Handle the transition from 23 to 0
        
        # Filter the data for the current hour
        if end_time !=0:
            mask = (data['DateTime'].dt.hour >= start_time) & (data['DateTime'].dt.hour < end_time) 
        else:
            mask = data['DateTime'].dt.hour >= start_time
        data_hour = data[mask]
    
        # Check if sleep_onset has occured yet
        if not sleep_onset_occured:
            # The absolute difference between the timestamps in the current hour and the sleep onset (in seconds)
            time_dif = abs((data_hour['DateTime'] - sleep_onset).dt.total_seconds())
            # Check if the sleep onset is within the current hour
            if any(time_dif <= tolerance):
                # Find the index of the first consecutive sleep period   
                first_s_index = data_hour[data_hour['DateTime'] == sleep_onset].index[0]
                first_s_index -= data_hour.index[0]
                # Slice the DataFrame to include rows starting from the first 'S' occurrence
                data_hour = data_hour.iloc[first_s_index:] 
                sleep_onset_occured = True
        
        # Count number of awakenings
        if sleep_onset_occured:
            # Iterate through all values of the current hour
            for value in data_hour['Sleep or Awake?']:
                    if value == 'W' and new_awakening:
                        # Increment the consecutive count by one
                        consecutive_w_count += 1
                        # Increment num_awakenings by one if the consecutive count >= min_consecutive_w 
                        if consecutive_w_count >= min_consecutive_w:
                            num_awakenings += 1
                            new_awakening = False
                    elif value == 'S':
                        consecutive_w_count = 0
                        new_awakening = True
                        
            # Check if an awakening overlapping with the next/subsequent hour
            if new_awakening and data_hour.iloc[-1]['Sleep or Awake?'] == 'W':                              
                # Calculate the start and end times for the subsequent hour
                start_subsequent = hour+1 if hour<23 else 0
                end_subsequent = start_subsequent+1 if start_subsequent<23 else 0
                # Filter the data for the current hour
                if end_subsequent !=0:
                    mask = (data['DateTime'].dt.hour >= start_subsequent) & (data['DateTime'].dt.hour < end_subsequent) 
                else:
                    mask = data['DateTime'].dt.hour >= start_subsequent
                subsequent_hour = data[mask]
                # Count the number of consecutive 'W's and see if there is enough to increment number of awakenings
                while subsequent_w:
                    if value == 'W':
                        # Increment the consecutive count by one
                        consecutive_w_count += 1
                        # Increment num_awakenings by one if the consecutive count >= min_consecutive_w 
                        if consecutive_w_count >= min_consecutive_w:
                            num_awakenings += 1
                            new_awakening = False
                            # Stop the loop (it is not neccessary to count further)
                            subsequent_w = False 
                    else:
                        # Stop the loop
                        subsequent_w = False 
        
        # The date and start hour as pandas datetime object
        datetime_start = data.loc[data['DateTime'].dt.hour == hour, 'DateTime'].values[0] 
        datetime_start = pd.to_datetime(datetime_start)
        datetime_start = datetime_start.floor('H')
        
        h_awakenings.append([datetime_start, num_awakenings])
        
    return h_awakenings


#%% WASO per hour per night

def hourly_WASO(data,min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculate hourly 'wake after sleep onset' (WASO) of acthigraph data from 
    in bed time to out of bed time.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
        
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 

    Returns
    -------
    h_WASO : list of minutes spent sleeping per hour. 

    """
       
    # Initialize lists to store hourly results
    h_WASO = []
    
    # Start and end datetime of night
    start = data.iloc[0]['DateTime']
    end = data.iloc[-1]['DateTime']

    # Tolerance for comparing timestamps to sleep onset (in seconds)
    tolerance = pd.Timedelta('1 minute').total_seconds()
    
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
            # The absolute difference between the timestamps in the current hour and the sleep onset (in seconds)
            time_dif = abs((data_hour['DateTime'] - sleep_onset).dt.total_seconds())
            # Check if the sleep onset is within the current hour
            if any(time_dif <= tolerance):
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
    
def hourly_avg_awakening(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Computes the average length of awakenings per hour for one night.

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
        
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 

    Returns
    -------
    avg_awakening : list
        List of average length of awakening per hour (float64). Including the 
        date and time as DateTime object. 

    """
    
    h_waso = hourly_WASO(data, min_consecutive_w, min_consecutive_s)
    h_awakenings = hourly_awakenings(data, min_consecutive_w, min_consecutive_s)
    
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
    
def calc_sleep_quality(data, in_bed, min_consecutive_w=1, min_consecutive_s=1):
    """
    Computes the sleep quality of one night. The sleep quality measure is based
    on three measurements: latency, efficiency and WASO. Bad quality is if at 
    least one of the following criterias are met: 
        latency > 30 min
        efficiency < 85%
        WASO > 40 min

    Parameters
    ----------
    data : Pandas Dataframe
        1xM dataframe with at least 3 columns called "Latency", "Efficiency" 
        and "Wake After Sleep Onset (WASO)". Contains summed actigraph data
        for one person from one night. 
        
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 

    Returns
    -------
    sleep_category : 0 or 1
        0 if the sleep is qualified as bad
        1 if the sleep is qualified as good
                
    
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
    
    latency = calc_latency(data, in_bed, min_consecutive_s)
    efficiency = calc_efficiency(data, min_consecutive_w, min_consecutive_s)
    WASO = calc_WASO(data, min_consecutive_w, min_consecutive_s)
    
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
    """
    Finds the datetime for when the person is considered as sleeping the first time. 

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
 
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 

    Returns
    -------
    sleep_onset : datetime
        When the person is considered as sleeping the first time.

    """
    
    # Setting sleep onset to zero
    sleep_onset = None
    consecutive_s_count = 0
    
    # Find the first time the person is considered as sleeping
    for j, value in enumerate(data['Sleep or Awake?']):
        if value == 'S':
            consecutive_s_count += 1
            if consecutive_s_count >= min_consecutive_s:
                sleep_onset = data.iloc[j - (min_consecutive_s-1)]['DateTime']
                break
        else:
            consecutive_s_count = 0
            
    return sleep_onset

#%% Sleep onset latency 
    
def calc_latency(data, in_bed, min_consecutive_s=1):
    """
    Calculates the sleep onset latency: The time it takes the person to fall 
    asleep after turning off lights. 

    Parameters
    ----------
    data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
 
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 
    
    in_bed : datetime 
        The time the person goes to sleep.
    

    Returns
    -------
    latency : INT64
    The minutes it takes the person to fall asleep when going to bed.

    """
    
    # Sleep onset from the function calc_SO
    sleep_onset = calc_SO(data, min_consecutive_s)
    
    # Calculate latency
    if sleep_onset:
        latency = (sleep_onset - in_bed).total_seconds() / 60
    else:
        latency = None
    
    return latency 

#%% Sleep efficiency
    
def calc_efficiency(data, min_consecutive_w=1, min_consecutive_s=1):
    """
    Calculate sleep efficiency of acthigraph data from in bed time to out of bed time.
    Sleep efficiency is the ratio between minutes spent sleeping and minutes spent
    in bed. 

    Parameters
    ----------
     data : Pandas Dataframe
        Requires a column called 'Sleep or Awake?' consisting of S and W corresponding
        to asleep and awake, respectively. There should also be a column 'DateTime'
        with the corresponding date and time as datetime objects.
        
    min_consecutive_w : int
        The number of minutes required to be awake before it is counted as an
        awakening, automaticlly set to 1 minute. 
    
    min_consecutive_s : int 
        The number of minutes required to be asleep before it is counted as the 
        first time falling asleep (Sleep Onset), automaticlly set to 1 minute. 
 
    Returns
    -------
    Int64
    Sleep efficency in percent. 

    """
    
    # Total sleep time
    tst = calc_TST(data, min_consecutive_w, min_consecutive_s)
    # Total amount of time spend in bed
    total_bed_time = data.shape[0]
    
    # Calculate efficiency
    if total_bed_time != 0:
        efficiency = (tst / total_bed_time) * 100
    else:
        efficiency = None
    
    return efficiency

    
