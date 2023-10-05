# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:48:40 2023

@author: LSKO0085

Modified by MGRO0154
"""

import pandas as pd
from datetime import timedelta

def MarkMissingData(data, dt=5):
    """
    Add data points with Nan CGM-value to the data frame data if there is 
    longer time than expected between two points.
    
    This function assumes that the CGM value measured at time point i has been
    constant since time point i-1. The data points with Nan values marking 
    missing data are therefore added at time point i-dt such that the measured
    CGM value at time point will be counted to have been constant for dt time
    and data is missing from time point i-1 to i-dt. dt is the expected time 
    step.
    
    """
    
    # Set the expected time step in minutes. Some extra time is added 
    # for numerical reasons.
    dt_minutes = dt + 1
    
    # Create empty list of missing points
    MissingPoints = [] 
    
    # Iterate over the rows of the CGM data
    for i in range(1, len(data)):
        # Calculate the time difference between consecutive timestamps
        time_diff = (data['DateTime'][i] - data['DateTime'][i-1]).total_seconds() / 60
        
        # Check if the time difference is greater than the expected time step
        if time_diff > dt_minutes:
            # Calculate the number of missing data points needed to fill the gap
            num_missing_points = int(time_diff / dt) - 1
            
            # Calculate the time interval between missing data points
            time_interval = timedelta(minutes=dt)
            
            # Insert NaN at missing data points
            for j in range(1, num_missing_points + 1):
                missing_datetime = data['DateTime'][i-1] + j * time_interval
                MissingPoints.append([missing_datetime, float("nan")])
    
    # Convert to Pandas dataframe
    MissingPoints = pd.DataFrame(MissingPoints, columns = ['DateTime','CGM'])
    
    # Add the missing data points to the existing data frame
    data = pd.concat([data,MissingPoints], ignore_index=True)
    
    # Sort the data and reset indexing
    data.sort_values(by='DateTime',ascending=True,inplace=True)
    data.reset_index(inplace=True, drop=True) 
    
    return data





