# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:31:13 2023

@author: MGRO0154
"""

import os
import pandas as pd
from ActiFeaturesFunc import *

#%%

def calc_WASO(data, min_consecutive_w=1):
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
        
        consecutive_w_count = 0
        waso = 0
        
        for value in WASO_data['Sleep or Awake?']:
            if value == 'W':
                consecutive_w_count += 1
                if consecutive_w_count >= min_consecutive_w:
                    waso += 1
            else:
                consecutive_w_count = 0
    
        return waso
    
#%%

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = "sleep_epochs_processed.csv"
filepath = os.path.join(in_dir, filename)
epoch_data = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)

summed_filename = "summed_sleep_processed.csv"
summed_file_path = os.path.join(in_dir, summed_filename)
summed_data = pd.read_csv(summed_file_path, parse_dates=[12, 13, 14], dayfirst=True)

waso_list = []

for i in range(summed_data.shape[0]):
    in_bed = summed_data.iloc[i]['In Bed DateTime']
    out_bed = summed_data.iloc[i]['Out Bed DateTime']
    
    # Extract one night's worth of actigraph epoch data
    night_data = extract_one_night(in_bed, out_bed, epoch_data)
    
    latency = calc_latency(night_data, in_bed)
    waso_list.append(latency)
    


