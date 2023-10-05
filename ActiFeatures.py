# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 10:37:13 2023

@author: LTEI0004
"""

#%% Import packages
import pandas as pd
from datetime import datetime
from ExtractIntervals import extract_one_night
import numpy as np
import os
from ActiFeaturesFunc import *

#%% Set the base directory for the current family and session
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"

# List of families
families = ["Fam01", "Fam03", "Fam05", "Fam06", "Fam07", "Fam09"]

# List of sessions for each family
sessions = ["Baseline", "Second", "Third"]

#%% Outer loop for families
for family in families:
    for session in sessions:
        in_dir = os.path.join(base_dir, family, session)

        # Read epoch data
        filename = "sleep_epochs_processed"
        filepath = os.path.join(in_dir, filename + '.csv')
        
        # Check if the file exists before reading it
        if os.path.exists(filepath):
            epoch_data = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)
        else:
            print(f"Sleep epoch actigraphy data file does not exist in {family}/{session}. Skipping...")
            continue

        # Read summed actigraphy data
        summed_filename = "sum_fam_processed"
        summed_file_path = os.path.join(in_dir, summed_filename + '.csv')
        
        # Check if the file exists before reading it
        if os.path.exists(summed_file_path):
            summed_data = pd.read_csv(summed_file_path, parse_dates=[12, 13, 14], dayfirst=True)
        else:
            print(f"Summed actigraphy data file does not exist in {family}/{session}. Skipping...")
            continue
        
       # Create empty list
        nightly_features_list = []
        hourly_awakenings_list = []
        hourly_waso_list = []
        hourly_avg_awakening_list = []
        sleep_quality_list = []
        
        # Loop through all relevant nights
        for i in range(summed_data.shape[0]):
            # Extract In Bed and Out Bed times
            in_bed = summed_data.iloc[i]['In Bed DateTime']
            out_bed = summed_data.iloc[i]['Out Bed DateTime']
            
            # Extract one night's worth of actigraph epoch data
             night_data = extract_one_night(in_bed, out_bed, epoch_data)
        
            # Number of awakenings per night
            num_awakenings = calc_awakenings(night_data)
            # Number of awakenings per hour per night
            h_awakenings = hourly_awakenings(night_data)
        
            # WASO per night
            waso = calc_WASO(night_data)
            # WASO per hour per night
            h_waso = hourly_WASO(night_data)
            
            # Average awakening length
            avg_awakening = calc_avg_awakening(night_data)
            # Hourly average awakening length
            h_avg_awakening = hourly_avg_awakening(night_data)

            # Total sleep time per night
            tst = calc_TST(night_data)
            
            # Sleep quality per night
            sleep_quality = calc_sleep_quality(summed_data.iloc[i])
            
            # Append lists with calculated features
            nightly_features_list.append([in_bed, out_bed, num_awakenings, waso,
                                          avg_awakening, tst, sleep_quality])
            
            for awakening in h_awakenings:
                hourly_awakenings_list.append(awakening)
            for waso in h_waso:
                hourly_waso_list.append(waso)
            for avg_awakening in h_avg_awakening:
                hourly_avg_awakening_list.append(avg_awakening)
                
            
        # Create a Pandas dataframes with calculated features
        nightly_features = pd.DataFrame(nightly_features_list, columns=['In Bed DateTime',
                                                               'Out Bed DateTime',
                                                               'Number of awakenings', 
                                                               'WASO', 'Average awakening length',
                                                               'TST', 'Sleep quality'])
        
        hourly_awakenings_df = pd.DataFrame(hourly_awakenings_list, columns=['DateTime start',
                                                                'Number of awakenings'])
        
        hourly_WASO_df = pd.DataFrame(hourly_waso_list, columns=['DateTime start',
                                                                'WASO'])
        
        hourly_avg_awakening_df = pd.DataFrame(hourly_avg_awakening_list, columns=['DateTime start',
                                                                'Average awakening length'])
                                                                
        # Merge dataframes with hourly awakenings and waso to one dataframe
        hourly_features1 = pd.merge(hourly_awakenings_df, hourly_WASO_df, on="DateTime start")
        hourly_features2 = pd.merge(hourly_features1, hourly_avg_awakening_df, on="DateTime start")
          
        # Export dataframes with actigraph features
        nightly_features.to_csv(os.path.join(in_dir, filename + "_features.csv"), index=False)
        hourly_features2.to_csv(os.path.join(in_dir, filename + "_hourly_features.csv"), index=False)
        
        print(f"Processed features for {family}/{session}")
        

