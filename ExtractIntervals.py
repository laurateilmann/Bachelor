# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 09:48:29 2023

@author: MGRO0154
"""

import pandas as pd
from datetime import datetime, timedelta

def extract_interval_in_out_bed(data, summed_data):
    """
    Extracts intervals of actigraphy data from in bed time to out of bed time.
    In bed and out of bed times are extracted from the parameter summed_data.

    Parameters
    ----------
    data : Pandas dataframe
        Nx2 dataframe with two columns: one with dates and times called 'DateTime',
        and one with the vector magnitude of actigraphy data called 'Magnitude'.
    summed_data : Pandas dataframe
        Dataframe with a minimum of the columns called 'In Bed DateTime' and 
        'Out Bed DateTime'.

    Returns
    -------
    Pandas dataframe.
        Mx2 dataframe with the same columns as the parameter 'data'. Now only
        with intervals between in bed and out of bed.
    """    
    
    # Extract "in bed times" and "out bed times" as datetime objects 
    in_bed_datetimes = summed_data['In Bed DateTime'] 
    out_bed_datetimes = summed_data['Out Bed DateTime'] 
    
    # Create a list to store dataframes for each day 
    daily_dataframes = [] 
    
    # Loop through each day and create a dataframe for the corresponding interval
    for in_bed_datetime, out_bed_datetime in zip(in_bed_datetimes, out_bed_datetimes): 
    
        # Filter data for the current day
        data_for_day = data[ (data['DateTime'] >= in_bed_datetime) & (data['DateTime'] <= out_bed_datetime) ] 
    
        # Append the dataframe to the list
        daily_dataframes.append(data_for_day) 
    
    # Combine dataframes for all days into a single dataframe
    data_in_out_bed = pd.concat(daily_dataframes, ignore_index=True)
    
    return data_in_out_bed

def extract_interval(start, end, data):
    """
    Extracts intervals of actigraphy data from starttime to endtime.

    Parameters
    ----------
    start : str.
        A time (eg. 22:00).
    end : str.
        A time (eg. 08:23).
    data : Pandas dataframe
        Nx2 dataframe with two columns: one with dates and times called 'DateTime',
        and one with the vector magnitude of actigraphy data called 'Magnitude'.

    Returns
    -------
    Pandas dataframe.
        Mx2 dataframe with the same columns as the parameter 'data'. Now only 
        with intervals between 'start' and 'end'.

    """
    
    # Define the start and end times you want to filter for 
    start_time = pd.to_datetime(start).time() 
    end_time = pd.to_datetime(end).time() 
    # Create a mask to filter timestamps within the specified time range 
    mask_nights = (data['DateTime'].dt.time >= start_time) | (data['DateTime'].dt.time <= end_time) 
    # Apply the mask to filter the data 
    data_nights = data[mask_nights]
    
    return data_nights


def extract_one_night(in_bed, out_bed, data):
    """
    Extracts one night of data starting from the date given as parameter. The
    night runs from In Bed to Out Bed the next morning.

    Parameters
    ----------
    in_bed : datetime 
    The time the person turns off light. 
    
    out_bed : datetime 
    The time the perosn is out of bed in the morning. 
    
    data : Pandas dataframe
         Dataframe with a minimum of the columns called 'In Bed DateTime' and 
        'Out Bed DateTime'..

    Returns
    -------
    night_data : Pandas dataframe
        Dataframe with just one nights data from In Bed to Out Bed. It has the
        same columns as the parameter 'data'.


    """


    night_data = data.loc[(data['DateTime'] >= in_bed) & (data['DateTime'] <= out_bed)]
    
    return night_data
