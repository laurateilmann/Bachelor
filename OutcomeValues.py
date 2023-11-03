# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:08:17 2023

@author: ltei0004
"""


import pandas as pd
from datetime import datetime
import os
import seaborn as sn
import matplotlib.pyplot as plt

base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM"
cgm_file = "\concatenated_cgm.csv"
epoch_file = "\concatenated_epochs.csv"

# Construct the full file paths
cgm_file_path = os.path.join(base_dir+cgm_file)
epoch_file_path = os.path.join(base_dir+epoch_file)

# Read the cgm and epoch data
cgm_data = pd.read_csv(cgm_file_path)
epoch_data = pd.read_csv(epoch_file_path)

# Merge cgm and epoch data
data = pd.merge(cgm_data, epoch_data, on=["In Bed DateTime", "Out Bed DateTime"])

# Find mean, sd and ranges (min to max)
mean = data.iloc[:, 2:].mean()
sd = data.iloc[:, 2:].std()
ran_min = data.iloc[:, 2:].min()
ran_max = data.iloc[:, 2:].max()

merged = pd.concat([mean, sd, ], axis=1)
merged.columns = ["Mean", "SD"]