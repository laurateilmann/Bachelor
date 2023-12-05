# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:54:05 2023

@author: MGRO0154
"""

#%% Import packages

import pandas as pd
from datetime import datetime
from ExtractIntervals import extract_one_night
import numpy as np
import os
from ActiFeaturesFunc import *
import csv
from PlotFunc import *
import plotly.io as io
from ExtractIntervals import *
import plotly.graph_objects as go
import plotly.io as io
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
import matplotlib.dates as mdates

plt.close('all')

#%% Import actigraph data

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"

# Read actigraphy data
filename = r"\Mind_fam01_ung60sec_processed"
acti_data = pd.read_csv(in_dir+filename+'.csv', parse_dates = [0], dayfirst=True)

# Read summed actigraphy data
filename = r"\summed_sleep_processed"
summed_data = pd.read_csv(in_dir+filename+'.csv', parse_dates = [12,13,14], dayfirst=True)

# Extract In Bed, Out Bed and Sleep Onset
i=0
in_bed = summed_data.iloc[i]['In Bed DateTime']
out_bed = summed_data.iloc[i]['Out Bed DateTime']
sleep_onset = summed_data.iloc[i]['Onset DateTime']

# Extract one nights data
acti_interval1 = extract_one_night(in_bed, out_bed, acti_data)

# Plot
plt.figure(figsize=(20,10))
plt.plot(acti_interval1['DateTime'], acti_interval1['Magnitude'], '-', label='Activity') 
plt.title("Actigraph data for one night", fontsize=40, family='Times New Roman', pad=20)
plt.xlabel("Time (hour)", fontsize=38, family='Times New Roman', labelpad=20)
plt.ylabel("Counts", fontsize=38, family='Times New Roman', labelpad=20)
plt.xticks(fontsize=35, family='Times New Roman')
plt.yticks(fontsize=35, family='Times New Roman')
plt.legend(fontsize=35)
plt.tight_layout()
# Set x-axis ticks to display only time
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
# Adding a vertical line at Sleep Onset (21:31)
plt.axvline(x=sleep_onset, color='red', linestyle='--', label='Sleep Onset', linewidth=3)
legend_font = {'family': 'Times New Roman', 'size': 35}
plt.legend(prop=legend_font)  # Place the legend at upper right

# Save fig
plt.savefig(r"H:\GitHub\Bachelor\Plots\Actigraph night plot.png")



