# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 13:19:52 2023

@author: ltei0004
"""

#%% Import packages
import pandas as pd
from datetime import datetime
import os

base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"
cgm_file = "\concatenated_cgm.csv"
epoch_file = "\concatenated_epochs.csv"

# Construct the full file paths
cgm_file_path = os.path.join(base_dir+cgm_file)
epoch_file_path = os.path.join(base_dir+epoch_file)

# Read the cgm and epoch data
cgm_data = pd.read_csv(cgm_file_path)
epoch_data = pd.read_csv(epoch_file_path)

data = pd.merge(cgm_data, epoch_data, on=["In Bed DateTime", "Out Bed DateTime"])

corrMatrix = data.corr()
print(corrMatrix)