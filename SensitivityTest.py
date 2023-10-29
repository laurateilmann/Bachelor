# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:31:13 2023

@author: MGRO0154
"""

import os
import pandas as pd
from ActiFeaturesFunc import *


#%%

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = "sleep_epochs_processed.csv"
filepath = os.path.join(in_dir, filename)
epoch_data = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)

summed_filename = "summed_sleep_processed.csv"
summed_file_path = os.path.join(in_dir, summed_filename)
summed_data = pd.read_csv(summed_file_path, parse_dates=[12, 13, 14], dayfirst=True)

feature_list = []

#summed_data.shape[0]
for i in range(1):
    in_bed = summed_data.iloc[i]['In Bed DateTime']
    out_bed = summed_data.iloc[i]['Out Bed DateTime']
    
    # Extract one night's worth of actigraph epoch data
    night_data = extract_one_night(in_bed, out_bed, epoch_data)
    
    feature = calc_awakenings(night_data,1, 5)
    feature2 = hourly_awakenings(night_data,1, 5)
    feature_list.append(feature)
    


