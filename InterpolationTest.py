# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 14:29:48 2023

@author: ltei0004
"""


import os
import pyActigraphy
import plotly.io as io
import pandas as pd
from datetime import datetime 
from MarkMissingData import MarkMissingData
from CalcPctActiveTime import *

base_dir = "L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"
# List of families
family = "Fam01"
# List of sessions for each family
session = "Baseline"

in_dir = os.path.join(base_dir, family, session)
filename = "sleep_epochs_processed"
filepath = os.path.join(in_dir, filename + '.csv')
data = pd.read_csv(filepath, parse_dates=[0], dayfirst=True)

CGM_filename = "cgm_data_processed"
CGM_file_path = os.path.join(in_dir, CGM_filename + '.csv')
CGM_data = pd.read_csv(CGM_file_path, parse_dates=[0], dayfirst=True)

# Assuming you have loaded your data into two dataframes named cgm_data and data
# Ensure that the 'DateTime' column is in datetime format

# Convert the 'DateTime' column to datetime format if it's not already
cgm_data['DateTime'] = pd.to_datetime(cgm_data['DateTime'])
data['DateTime'] = pd.to_datetime(data['DateTime'])

# Set the 'DateTime' column as the index for both dataframes
cgm_data.set_index('DateTime', inplace=True)
data.set_index('DateTime', inplace=True)

# Resample the Actigraph data to 5-minute intervals and interpolate
actigraph_resampled = data.resample('5T').interpolate(method='linear')

# Now, you have the Actigraph data interpolated to 5-minute intervals
# in the 'actigraph_resampled' dataframe. You can reset the index if needed:
actigraph_resampled.reset_index(inplace=True)

# You can merge the CGM and interpolated Actigraph dataframes based on the 'DateTime' column
merged_df = pd.concat([cgm_data, actigraph_resampled], axis=1)

# 'merged_df' now contains both CGM and interpolated Actigraph data for comparison
