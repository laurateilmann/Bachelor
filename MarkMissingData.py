# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 12:48:40 2023

@author: LSKO0085
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
    
    MissingPoints = [] 
    
    # Set the expected time step. Some extra time is added 
    # for numerical reasons.
    dt = timedelta(minutes = dt + 1)
    
    # Create time stamps for the missing data points and set their CGM value to Nan
    for i in range(1,len(data)):
        if data['DateTime'][i]-data['DateTime'][i-1] > dt: # Missing data between point i-1 and i
            MissingPoints.append([data['DateTime'][i]-dt, float("nan")])
        

    MissingPoints = pd.DataFrame(MissingPoints, columns = ['DateTime','CGM'])
    
    # Add the missing data points to the existing data frame
    data = pd.concat([data,MissingPoints], ignore_index=True)
    
    # Sort the data and reset indexing
    data.sort_values(by='DateTime',ascending=True,inplace=True)
    data.reset_index(inplace=True, drop=True) 
    
    return data