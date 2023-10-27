# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:38:28 2023

@author: LTEI0004
"""


import os
import pyActigraphy
import plotly.io as io
import pandas as pd
from datetime import datetime 
from MarkMissingData import MarkMissingData
from CalcPctActiveTime import *
from PrepareLibreviewData import *
from ActiFeaturesFunc import *

#%% 

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = "sleep_epochs_processed.csv"
filepath = os.path.join(in_dir, filename)
epoch_data = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)

summed_filename = "summed_sleep_processed.csv"
summed_file_path = os.path.join(in_dir, summed_filename)
summed_data = pd.read_csv(summed_file_path, parse_dates=[12, 13, 14], dayfirst=True)



#%%

sleep_onset_list=[]
latency_list = []

for i in range(summed_data.shape[0]):
    in_bed = summed_data.iloc[i]['In Bed DateTime']
    out_bed = summed_data.iloc[i]['Out Bed DateTime']
    
    # Extract one night's worth of actigraph epoch data
    night_data = extract_one_night(in_bed, out_bed, epoch_data)
    
    sleep_onset = None
    consecutive_s_count = 0
    for j, value in enumerate(night_data['Sleep or Awake?']):
        if value == 'S':
            consecutive_s_count += 1
            if consecutive_s_count >= 5:
                sleep_onset = night_data.iloc[j - 4]['DateTime']
                break
        else:
            consecutive_s_count = 0
    
    if sleep_onset:
        latency = (sleep_onset - in_bed).total_seconds() / 60
        latency_list.append(latency)
    else:
        latency_list.append(None)
    
    sleep_onset_list.append(sleep_onset)


#%% Delta-latency: difference between calculated and given latency

delta_latency = latency_list - summed_data.iloc[:]['Latency']


#%% Test for number of awakenings

num_awakenings_list = []

num_awakenings = calc_awakenings(epoch_data,5)

num_awakenings_list.append(num_awakenings)
    

awakenings = ((epoch_data['Sleep or Awake?'] == 'W') & (epoch_data['Sleep or Awake?'].shift(1) == 'S'))
number_awakenings = awakenings.sum()
    
