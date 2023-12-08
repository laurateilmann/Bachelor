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

base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data"
file_n = "\concatenated_all_11.csv"
file_h = "\concatenated_hourly_all_11.csv"

# Construct the full file paths
file_n_path = os.path.join(base_dir+file_n)
file_h_path = os.path.join(base_dir+file_h)

# Read the concatenated data
data_n = pd.read_csv(file_n_path)
data_h = pd.read_csv(file_h_path)

# Find mean, sd and ranges (min to max) nightly
mean_n = data_n.iloc[:, 2:].mean()
sd_n = data_n.iloc[:, 2:].std()
ran_min_n = data_n.iloc[:, 2:].min()
ran_max_n = data_n.iloc[:, 2:].max()

# Find mean, sd and ranges (min to max) hourly
mean_h = data_h.iloc[:, 1:].mean()
sd_h = data_h.iloc[:, 1:].std()
ran_min_h = data_h.iloc[:, 1:].min()
ran_max_h = data_h.iloc[:, 1:].max()

