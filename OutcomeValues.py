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
file11 = "\concatenated_all_11.csv"
file51 = "\concatenated_all_51.csv"

# Construct the full file paths
file11_path = os.path.join(base_dir+file11)
file51_path = os.path.join(base_dir+file51)

# Read the concatenated data
data11 = pd.read_csv(file11_path)
data51 = pd.read_csv(file51_path)

# Find mean, sd and ranges (min to max)
mean11 = data11.iloc[:, 2:].mean()
sd11 = data11.iloc[:, 2:].std()
ran_min11 = data11.iloc[:, 2:].min()
ran_max11 = data11.iloc[:, 2:].max()

# Find mean, sd and ranges (min to max)
mean51 = data51.iloc[:, 2:].mean()
sd51 = data51.iloc[:, 2:].std()
ran_min51 = data51.iloc[:, 2:].min()
ran_max51 = data51.iloc[:, 2:].max()

# merged = pd.concat([mean, sd, ], axis=1)
# merged.columns = ["Mean", "SD"]