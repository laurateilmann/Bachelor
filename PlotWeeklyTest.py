# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 09:58:48 2023

@author: ltei0004
"""


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ExtractIntervals import *
import math 
import matplotlib.dates as mdates
from datetime import datetime

# Set the base directory where your files are located
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"

# Import CGM data
in_dir = os.path.join(base_dir, "Fam01", "Second")

# Read CGM data
CGM_filename = "cgm_data_processed"
CGM_file_path = os.path.join(in_dir, CGM_filename + '.csv')
CGM_data = pd.read_csv(CGM_file_path, parse_dates=['DateTime'], dayfirst=True)

# Read summed actigraphy data
summed_filename = "sum_fam_processed"
summed_file_path = os.path.join(in_dir, summed_filename + '.csv')
summed_data = pd.read_csv(summed_file_path, parse_dates=[12, 13, 14], dayfirst=True)

nrows = math.ceil(summed_data.shape[0]/4)


# Create subplots
fig, axs = plt.subplots(nrows=nrows, ncols=4, sharey=True, figsize=[15, 6])

# Remove excess axes
# for i in range(6):
#     axs[1, 1 + i].set_axis_off()

# # Set weekday titles
# weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# for i in range(7):
#     axs[0, i].set_title(weekdays[i])

# Limits
upper_lim = 10.0
lower_lim = 3.9
EPS = 0.01  # Set such that limit range covers correctly


# Loop through all relevant nights
for i in range(summed_data.shape[0]):
    # Extract In Bed and Out Bed times
    in_bed = summed_data.iloc[i]['In Bed DateTime']
    out_bed = summed_data.iloc[i]['Out Bed DateTime']
    
    # Extract one night's worth of CGM data
    night_data = extract_one_night(in_bed, out_bed, CGM_data)
    data = night_data['CGM']
    ts = night_data['DateTime']

    row = i // 4
    col = i % 4

    # Insert day number
    date = in_bed.strftime('%A %Y-%m-%d')
    date_end = out_bed.strftime(' - %A %Y-%m-%d')
    axs[row, col].text(.05, .95, str(date + date_end), ha='left', va='top', transform=axs[row, col].transAxes)
    # Format x axis
    #axs[row,col].set_xlim(in_bed.hour, out_bed.hour)
    # axs[row,col].set_xticks([21, 2, 7])
    
    # Format the x-axis ticks 
    axs[row,col].xaxis.set_major_formatter(mdates.DateFormatter('%H')) 
    # Optionally, set the interval for x-axis ticks 
    axs[row,col].xaxis.set_major_locator(mdates.HourLocator(interval=2))

    
    
    # Format x axis (assuming ts contains datetime objects)
    # axs[row, col].set_xlim(ts.min(), ts.max())

    # Insert CGM_data
    axs[row, col].plot(ts, data, color='k')


    # Fill beyond limits
    axs[row, col].fill_between(ts, upper_lim, np.maximum(data, upper_lim), color='blue')
    axs[row, col].fill_between(ts, lower_lim, np.minimum(data, lower_lim), color='red')

    # Fill limits
    axs[row, col].fill_between(ts, upper_lim + EPS, lower_lim - EPS, color='green')
    
# Get space between subplots
fig.tight_layout()

# Add figure-level labels with adjusted coordinates
fig.text(0.5, 0.01, 'Time (hour)', ha='center', fontsize=16)  
fig.text(0.003, 0.5, 'IG (mmol/L)', va='center', fontsize=16, rotation=90)  

plt.get_current_fig_manager().full_screen_toggle()


# Save plot
plt.savefig("demo.pdf", format="pdf")

plt.show()  # Optional: Display the plot
