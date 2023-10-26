""" 

Created on Thu Oct  5 09:58:48 2023 
  
@author: ltei0004 

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

# Merge all sessions 
CGM_data_all = pd.concat((CGM_data_list[0],CGM_data_list[1],CGM_data_list[2]))
summed_data_all = pd.concat((summed_data_list[0],summed_data_list[1],summed_data_list[2]))

# Check what weekday the sessions starts on
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
#nrows = math.ceil(num_days_total/7) 
nrows = 5
ncols = 7

# Create subplots in figure
fig, axs = plt.subplots(nrows=nrows, ncols=ncols, sharey=True, figsize=[15, 6]) 

# Remove excess axes 
# for i in range(6): 
#     axs[1, 1 + i].set_axis_off() 

# # Set weekday titles 
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] 
for i in range(7): 
    axs[0, i].set_title(weekdays[i], fontsize=25) 

# Limits 
upper_lim = 10.0 
lower_lim = 3.9 
EPS = 0.01  # Set such that limit range covers correctly 

# Starting row and column in subplot
col = 0
row = 0

# Loop through all relevant nights 
for i in range(num_days_total): 
    
    # Extract In Bed and Out Bed times 
    in_bed = summed_data_all.iloc[i]['In Bed DateTime'] 
    out_bed = summed_data_all.iloc[i]['Out Bed DateTime'] 
     
    # Extract one night's worth of CGM data 
    night_data = extract_one_night(in_bed, out_bed, CGM_data_all) 
    data = night_data['CGM'] 
    ts = night_data['DateTime'] 
    
    # Check if col and/or row need to be changed depending on the start of each session:
    if i==0: # start of Baseline (session 1)
        col = weekday_start_baseline
    elif i==num_days_baseline: # start of Second (session 2)
        col = weekday_start_second
        row += 1
    elif i==(num_days_baseline + num_days_second): # start of Third (session 3)
        col = weekday_start_third
        row += 1

    # Insert dates 
    date_start = in_bed.strftime('%d/%m') 
    date_end = out_bed.strftime('-%d/%m') 
    axs[row, col].text(.05, .95, str(date_start + date_end), ha='left', va='top', transform=axs[row, col].transAxes, fontsize=20)   

    # Format the x-axis ticks  
    axs[row,col].xaxis.set_major_formatter(mdates.DateFormatter('%H'))  
    # Set the interval for x-axis ticks  
    axs[row,col].xaxis.set_major_locator(mdates.HourLocator(interval=3)) 
    # Set the fontsize of the x- and y-axis ticks 
    axs[row, col].tick_params(axis='x', labelsize=20,) 
    axs[row, col].tick_params(axis='y', labelsize=20) 

    # Plot CGM_data 
    axs[row, col].plot(ts, data, color='k') 

    # Fill beyond limits 
    axs[row, col].fill_between(ts, upper_lim, np.maximum(data, upper_lim), color='orange', edgecolor='none') 
    axs[row, col].fill_between(ts, lower_lim, np.minimum(data, lower_lim), color='red', edgecolor='none') 

    # Fill limits 
    axs[row, col].fill_between(ts, upper_lim + EPS, lower_lim - EPS, color='grey', alpha=0.2) 
    
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
fig.text(0.5, 0.01, 'Time (hour)', ha='center', fontsize=25)   
fig.text(0.006, 0.5, 'IG (mmol/L)', va='center', fontsize=25, rotation=90)   

# Necessary for getting a good saved image
plt.get_current_fig_manager().full_screen_toggle()   

# Save plot 
plt.savefig("H:\GitHub\Bachelor\Plots\weeklyCGMPlot.png", format="png")   

# Display 
plt.show()  
 