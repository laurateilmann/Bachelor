# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 09:09:57 2023

@author: ltei0004
"""
import pandas as pd
from PlotFunc import *
import plotly.io as io
from ExtractIntervals import *
import plotly.graph_objects as go
import plotly.io as io
import matplotlib.pyplot as plt

#%% Import CGM features 

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = r"\cgm_data_processed_features"

cgm_features = pd.read_csv(in_dir+filename+'.csv', parse_dates = [0], dayfirst=True)

# Extract TIR from cgm features
tir = cgm_features['TIR (%)']


#%% Import sleep epochs features

filename = r'\sleep_epochs_processed_features'

epochs_features =  pd.read_csv(in_dir+filename+'.csv', parse_dates = [0], dayfirst=True)

# Extract WASO from epochs features
waso = epochs_features['WASO']

    
#%% Plot: TIR and WASO

plt.figure()
plt.plot(tir, waso, '.')
plt.title("TIR against WASO")
plt.xlabel("Time in range (%)")
plt.ylabel("WASO (min)")

#%% Plot: max IG and WASO

plt.figure()
plt.plot(cgm_features['max'], epochs_features['WASO'], '.')
plt.title("Max IG against WASO")
plt.xlabel("Max intestinal glucose (mmol/L)")
plt.ylabel("WASO (min)")

#%% Plot: min IG and WASO

plt.figure()
plt.plot(cgm_features['min'], epochs_features['WASO'], '.')
plt.title("Min. IG against WASO")
plt.xlabel("Min. intestinal glucose (mmol/L)")
plt.ylabel("WASO (min)")

#%% Plot: mean and TST

plt.figure()
plt.plot(cgm_features['mean'], epochs_features['TST'], '.')
plt.title("Mean against TST")
plt.xlabel("Mean intestinal glucose (mmol/L)")
plt.ylabel("Total sleep time (min)")

#%% Plot: mean and number of awakenings

plt.figure()
plt.plot(cgm_features['mean'], epochs_features['Number of awakenings'], '.')
plt.title("Mean against number of awakenings")
plt.xlabel("Mean intestinal glucose (mmol/L)")
plt.ylabel("Number of awakenings")

#%% Plot: std and WASO

plt.figure()
plt.plot(cgm_features['std'], epochs_features['WASO'], '.')
plt.title("Std against WASO")
plt.xlabel("Standard deviation")
plt.ylabel("WASO (min)")
