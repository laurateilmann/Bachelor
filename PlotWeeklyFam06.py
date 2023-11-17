# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 09:24:46 2023

@author: LTEI0004
"""


import os 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt  
from ExtractIntervals import * 
import matplotlib.dates as mdates 

# Set the base directory where your files are located 
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes" 

# List of sessions
sessions = ["Baseline", "Second", "Third"]

# Define the specific date ranges for each session
date_ranges = {
    "Baseline": ["2023-04-16", "2023-04-24"],
    "Second": ["2023-05-13", "2023-05-23"],
    "Third": ["2023-06-18", "2023-06-27"]
}

# Empty lists of CGM data and summed data
CGM_data_list = []
summed_data_list = []

# Iterate over all sessions
for session in sessions:
    # Path to files
    in_dir = os.path.join(base_dir, "Fam06", session)

    # Read CGM data
    CGM_filename = "cgm_data_processed"
    CGM_file_path = os.path.join(in_dir, CGM_filename + '.csv')
    CGM_data = pd.read_csv(CGM_file_path, parse_dates=['DateTime'], dayfirst=True)
    CGM_data_list.append(CGM_data)

    # Read summed actigraphy data
    summed_filename = "summed_sleep_processed"
    summed_file_path = os.path.join(in_dir, summed_filename + '.csv')
    summed_data = pd.read_csv(summed_file_path, parse_dates=[12, 13, 14], dayfirst=True)
    summed_data_list.append(summed_data)

# Check what weekday the sessions start on
weekday_start_baseline = summed_data_list[0].iloc[0]['In Bed DateTime'].weekday()
weekday_start_second = summed_data_list[1].iloc[0]['In Bed DateTime'].weekday()
weekday_start_third = summed_data_list[2].iloc[0]['In Bed DateTime'].weekday()

# Check number of days in each session
num_days_baseline = summed_data_list[0].shape[0]
num_days_second = summed_data_list[1].shape[0]
num_days_third = summed_data_list[2].shape[0]
# Total number of days
num_days_total = num_days_baseline + num_days_second + num_days_third

# Number of rows and columns in figure
nrows = 3
ncols = 7

# Create subplots in figure
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, sharey=True, figsize=[15, 6])

# Remove excess axes 
for i in range(2): 
    axs[1, 0 + i].set_axis_off() 

# Set weekday titles
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
for i in range(7):
    axs[0, i].set_title(weekdays[i], fontsize=38)

# Limits
upper_lim = 10.0
lower_lim = 3.9
EPS = 0.01  # Set such that the limit range covers correctly

# Starting row and column in subplot
col = 0
row = 0

# Loop over the sessions
for session_index, session in enumerate(sessions):
    # Extract the date range for the current session
    start_date, end_date = date_ranges[session]

    # Convert to datetime for comparison
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on the specified date range
    filtered_summed_data = summed_data_list[session_index].loc[
        (summed_data_list[session_index]['In Bed DateTime'] >= start_date) & (
                    summed_data_list[session_index]['Out Bed DateTime'] <= end_date)]
    
    # Adjust row and col
    row = session_index  # Start the row from the session index
    col = 0
    

    # Adjust col based on the session start weekday
    if session_index == 0:  # start of Baseline (session 1)
        col = weekday_start_baseline
    elif session_index == 1:  # start of Second (session 2)
        col = weekday_start_second
    elif session_index == 2:  # start of Third (session 3)
        col = weekday_start_third

    for i in range(filtered_summed_data.shape[0]):
        # Extract In Bed and Out Bed times
        in_bed = filtered_summed_data.iloc[i]['In Bed DateTime']
        out_bed = filtered_summed_data.iloc[i]['Out Bed DateTime']

        # Initialize ts here
        ts = extract_one_night(in_bed, out_bed, CGM_data_list[session_index])['DateTime']

        # Initialize data here
        data = extract_one_night(in_bed, out_bed, CGM_data_list[session_index])['CGM']


        # # Insert dates 
        # date_start = in_bed.strftime('%d/%m') 
        # date_end = out_bed.strftime('-%d/%m') 
        # axs[row, col].text(.4, .95, str(date_start + date_end), ha='left', va='top', transform=axs[row, col].transAxes, fontsize=24)   
    
        # Format the x-axis ticks  
        axs[row,col].xaxis.set_major_formatter(mdates.DateFormatter('%H'))  
        # Set the interval for x-axis ticks  
        axs[row,col].xaxis.set_major_locator(mdates.HourLocator(interval=3)) 
        # Set the fontsize of the x- and y-axis ticks 
        axs[row, col].tick_params(axis='x', labelsize=30) 
        axs[row, col].tick_params(axis='y', labelsize=3) 
    
        # Plot CGM_data 
        axs[row, col].plot(ts, data, color='k') 
    
        # Fill beyond limits 
        axs[row, col].fill_between(ts, upper_lim, np.maximum(data, upper_lim), color='orange', edgecolor='none') 
        axs[row, col].fill_between(ts, lower_lim, np.minimum(data, lower_lim), color='red', edgecolor='none') 
    
        # Fill limits 
        axs[row, col].fill_between(ts, upper_lim + EPS, lower_lim - EPS, color='grey', alpha=0.13) 
        
        # Check if row needs to be changed
        if col == 6:
            row += 1
        
        # Check if col needs to be changed
        if col != 6:    
            col += 1
        else:
            col = 0
    

# Get space between subplots 
fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.1, wspace=0.1, hspace=0.2) 

# Add figure-level labels with adjusted coordinates 
fig.text(0.5, 0.01, 'Time (hour)', ha='center', fontsize=40)   
fig.text(0.006, 0.5, 'IG (mmol/L)', va='center', fontsize=40, rotation=90)   

# Necessary for getting a good saved image
plt.get_current_fig_manager().full_screen_toggle()   

# Save plot 
plt.savefig("H:\GitHub\Bachelor\Plots\weeklyCGM")

            
# Display 
plt.show()  