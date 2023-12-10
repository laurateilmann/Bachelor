# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 10:24:40 2023

@author: MGRO0154 & LTEI0004

Functions to compute various statistics for CGM data.
"""
import pandas as pd

def calc_stats(CGM_data_original):
    """
    Calculates statistics of CGM data.

    Parameters
    ----------
    CGM_data : Pandas Dataframe 
    Nx2 dataframe with two columns: one with dates and times called 'DateTime',
    and one with CGM data called 'CGM'.

    Returns
    -------
    CGM_stats : list consisting of 'mean', 'std', 'min', 'max', 'cv', 'Q1', 'Q2', 'Q3'.

    """ 
   
    # Exclude 'id' column 
    CGM_data = CGM_data_original[['DateTime', 'CGM']]
    # Calculate statistics
    CGM_stats = CGM_data.describe().T
    # Drop 'count' column
    CGM_stats = CGM_stats.drop(['count', '25%', '75%'], axis=1)
    # Reset index 
    CGM_stats = CGM_stats.reset_index(drop=True)
     # Rename the columns
    CGM_stats.rename(columns={'50%': 'median'}, inplace=True)
    # Calculate and include Coefficient of Variation (cv)
    cv = (CGM_stats['std'] / CGM_stats['mean']).values.tolist()
    CGM_stats['cv'] = cv
    deltaIG = (CGM_stats['max'] - CGM_stats['min']).values.tolist()
    CGM_stats['delta IG'] = deltaIG
    # Reordering columns
    CGM_stats = CGM_stats[['mean', 'std', 'median', 'min', 'max', 'cv', 'delta IG']]
    # Convert to list
    CGM_stats = CGM_stats.values.tolist()
    CGM_stats = [item for sublist in CGM_stats for item in sublist]
    
    return CGM_stats


def hourly_stats(CGM_data_original):
    """
    Calculate hourly statistics of CGM data.

    Parameters
    ----------
    CGM_data_original : Pandas Dataframe 
    Nx2 dataframe with two columns: one with dates and times called 'DateTime',
    and one with CGM data called 'CGM'.

    Returns
    -------
    CGM_stats : list consisting of hourly 'mean', 'std', 'min', 'max', 'cv', 'Q1', 'Q2', 'Q3'.

    """

    # Exclude 'id' column
    CGM_data = CGM_data_original[['DateTime', 'CGM']]
    
    # Set 'DateTime' as the index
    CGM_data.set_index('DateTime', inplace=True)
    
    # Calculate hourly statistics
    CGM_data_mean = CGM_data.resample('H').mean()
    CGM_data_std = CGM_data.resample('H').std()
    CGM_data_min = CGM_data.resample('H').min()
    CGM_data_max = CGM_data.resample('H').max()
    CGM_data_median = CGM_data.resample('H').quantile(0.50)
    CGM_data_cv = CGM_data_std/CGM_data_mean
    CGM_data_deltaIG = CGM_data_max-CGM_data_min
    
    # Create pandas dataframe with calculated hourly statistics
    CGM_stats = pd.concat([CGM_data_mean, CGM_data_std, CGM_data_median, CGM_data_min, CGM_data_max, CGM_data_cv, CGM_data_deltaIG], axis = 1)
    CGM_stats.columns = ['mean', 'std', 'median', 'min', 'max','cv', 'delta IG']
    CGM_stats = CGM_stats.reset_index()
    
    # Convert to list
    CGM_stats = CGM_stats.values.tolist()
    
    return CGM_stats

