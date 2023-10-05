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
import numpy as np
import seaborn as sns

#%% Import CGM features 

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = r"\cgm_data_processed_features"

cgm_features = pd.read_csv(in_dir+filename+'.csv', parse_dates = [0,1], dayfirst=True)

# Extract TIR from cgm features
tir = cgm_features['TIR (%)']


#%% Import sleep epochs features

filename = r'\sleep_epochs_processed_features'

epochs_features =  pd.read_csv(in_dir+filename+'.csv', parse_dates = [0,1], dayfirst=True)

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

#%% Pairwise scatterplot

cgm_features_plot = cgm_features.iloc[:,[2,3,4,5,6,7,9,11,12,13]]
epoch_features_plot = epochs_features.iloc[:,2:]

# Change the feature 'Sleep quality' so 0='Very bad sleep', 1='Fairly bad sleep',
# 2='Fairly good sleep', 3='Very bad sleep'
epoch_features_plot.replace('Very bad sleep', 0, inplace=True)
epoch_features_plot.replace('Fairly bad sleep', 1, inplace=True)
epoch_features_plot.replace('Fairly good sleep', 2, inplace=True)
epoch_features_plot.replace('Very good sleep', 3, inplace=True)

all_features = pd.concat([cgm_features_plot,epoch_features_plot],axis=1)

M = cgm_features_plot.shape[1]
N = epoch_features_plot.shape[1]

for i, cgm_feature in enumerate(cgm_features_plot):
    
    # Create subplots for each CGM feature
    fig, axes = plt.subplots(1, N, figsize=(18, 3))
    
    for j, epoch_feature in enumerate(epoch_features_plot):
        sns.scatterplot(data=all_features, x=cgm_feature, y=epoch_feature,ax=axes[j])
        axes[j].set_xlabel(cgm_feature)
        axes[j].set_ylabel(epoch_feature)

    plt.tight_layout()
    plt.show()
