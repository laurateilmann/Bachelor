# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 10:24:40 2023

@author: MGRO0154
"""
import pandas as pd

def calc_stats(CGM_data):
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
    # Calculate statistics
    CGM_stats = CGM_data.describe().T
    # Drop 'count' column
    CGM_stats = CGM_stats.iloc[:, 1:]
    # Reset index 
    CGM_stats = CGM_stats.reset_index(drop=True)
    # Calculate and include Coefficient of Variation (cv)
    cv = (CGM_stats['std'] / CGM_stats['mean']).values.tolist()
    CGM_stats['cv'] = cv
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
    # Set 'DateTime' as the index
    CGM_data = CGM_data_original.copy()
    CGM_data.set_index('DateTime', inplace=True)
    
    # Calculate hourly statistics
    CGM_data_mean = CGM_data.resample('H').mean()
    CGM_data_std = CGM_data.resample('H').std()
    CGM_data_min = CGM_data.resample('H').min()
    CGM_data_max = CGM_data.resample('H').max()
    CGM_data_q1 = CGM_data.resample('H').quantile(0.25)
    CGM_data_q2 = CGM_data.resample('H').quantile(0.50)
    CGM_data_q3 = CGM_data.resample('H').quantile(0.75)
    CGM_data_cv = CGM_data_std/CGM_data_mean
    
    # Create pandas dataframe with calculated hourly statistics
    CGM_stats = pd.concat([CGM_data_mean, CGM_data_std, CGM_data_min, CGM_data_q1, CGM_data_q2, CGM_data_q3, CGM_data_max, CGM_data_cv], axis = 1)
    CGM_stats.columns = ['mean', 'std','min', 'Q1', 'Q2', 'Q3', 'max','cv']
    CGM_stats = CGM_stats.reset_index()
    
    # Convert to list
    CGM_stats = CGM_stats.values.tolist()
    
    return CGM_stats
    