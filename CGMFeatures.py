# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 13:19:33 2023

@author: LTEI0004
"""

#%%
import os
import pandas as pd
from ExtractIntervals import extract_one_night
from CGMRanges import calc_ranges, hourly_ranges
from CGMStats import calc_stats, hourly_stats

#%% Set the base directory where your files are located
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"

# List of families
families = ["Fam01", "Fam03", "Fam05", "Fam06", "Fam07", "Fam09"]

# List of sessions for each family
sessions = ["Baseline", "Second", "Third"]

#%% Loop through each family
for family in families:
    # Loop through each session for the family
    for session in sessions:
        in_dir = os.path.join(base_dir, family, session)
        
        # Read CGM data
        CGM_filename = "cgm_data_processed"
        CGM_file_path = os.path.join(in_dir, CGM_filename + '.csv')
        
        # Check if the file exists before reading it
        if os.path.exists(CGM_file_path):
            CGM_data = pd.read_csv(CGM_file_path, parse_dates=[0], dayfirst=True)
        else:
            print(f"CGM data file does not exist in {family}/{session}. Skipping...")
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
        
        # Check if CGM data and actigraph data is matching in time (dates)
        first_date = summed_data.iloc[0]['In Bed DateTime']
        last_date = summed_data.iloc[-1]['Out Bed DateTime']
        if not (CGM_data.iloc[0]['DateTime'] <= first_date) & (CGM_data.iloc[-1]['DateTime'] >= last_date):
            print(f"CGM and actigraph data in {family}/{session} does not match in time. Skipping...")
            continue
        
        # Create an empty lists to store CGM features
        CGM_features_list = []
        CGM_h_stats_list = []
        CGM_h_ranges_list = []
        
        # Loop through all relevant nights
        for i in range(summed_data.shape[0]):
            # Extract In Bed and Out Bed times
            in_bed = summed_data.iloc[i]['In Bed DateTime']
            out_bed = summed_data.iloc[i]['Out Bed DateTime']
            
            # Extract one night's worth of CGM data
            night_data = extract_one_night(in_bed, out_bed, CGM_data)
            
            # Calculate TIR, TAR, and TBR
            CGM_ranges = calc_ranges(night_data)
            h_ranges = hourly_ranges(night_data)
            
            # Calculate statistics (mean, std, min, max, etc.)
            CGM_stats = calc_stats(night_data)
            h_stats = hourly_stats(night_data)
            
            # Append lists with calculated features
            CGM_features_list.append([in_bed, out_bed] + CGM_ranges + CGM_stats)
            
            for h_stat in h_stats:
                CGM_h_stats_list.append(h_stat)
            
            for h_range in h_ranges:
                CGM_h_ranges_list.append(h_range)
      
        # Create a Pandas dataframes with calculated features
        CGM_features = pd.DataFrame(CGM_features_list, columns=['In Bed DateTime',
                                                               'Out Bed DateTime',
                                                               'TIR (%)', 'TAR (%)',
                                                               'TBR (%)', 'mean', 'std',
                                                               'min', 'Q1', 'Q2', 'Q3', 
                                                               'max','cv', 'delta IG'])
        
        CGM_h_stats = pd.DataFrame(CGM_h_stats_list, columns=['DateTime start', 
                                                                'mean', 'std',
                                                                'min', 'Q1', 'Q2',
                                                                'Q3', 'max','cv', 'delta IG'])
        
        CGM_h_ranges = pd.DataFrame(CGM_h_ranges_list, columns=['DateTime start',
                                                                'TIR (%)','TAR (%)',
                                                                'TBR (%)'])
        
        # Merge dataframes with hourly statistics and ranges to one dataframe
        CGM_h_features = pd.merge(CGM_h_ranges, CGM_h_stats, on="DateTime start")
        
        # Export dataframes with CGM features
        CGM_features.to_csv(os.path.join(in_dir, "cgm_data_processed_features.csv"), index=False)
        CGM_h_features.to_csv(os.path.join(in_dir, "cgm_data_processed_hourly_features.csv"), index=False)
        
        print(f"Processed features for {family}/{session}")
        
