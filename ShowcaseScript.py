# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 12:29:42 2023

@author: MGRO0154
"""

import pandas as pd
from PlotFunc import *
import plotly.io as io
from ExtractIntervals import *
import plotly.graph_objects as go
import plotly.io as io

#%% Figure settings

# Interactive figures open in browser
io.renderers.default='browser' #set to 'svg' to open in Spyder plot tab

#%% Import CGM 

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = r"\cgm_data_processed"

# Read CGM data
CGM_data = pd.read_csv(in_dir+filename+'.csv', parse_dates = [0], dayfirst=True)

#%% Import actigraph data 

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = r"\Mind_fam01_ung60sec_processed"

# Read actigraphy data
acti_data = pd.read_csv(in_dir+filename+'.csv', parse_dates = [0], dayfirst=True)

#%% Import summed actigraph data 

in_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes\Fam01\Baseline"
filename = r"\sum_fam_processed"

# Read summed actigraphy data
summed_data = pd.read_csv(in_dir+filename+'.csv', parse_dates = [12,13,14], dayfirst=True)

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


#%% Plot actigraph data

plot_acti(acti_data)

#%% Plot CGM data

plot_CGM(CGM_data)

#%% Extract intervals in-bed to out-of-bed

acti_interval = extract_interval_in_out_bed(acti_data, summed_data)
plot_acti(acti_interval)

#%% Extract one night of actigraph data

i=0
in_bed = summed_data.iloc[i]['In Bed DateTime']
out_bed = summed_data.iloc[i]['Out Bed DateTime']

acti_interval1 = extract_one_night(in_bed, out_bed, acti_data)
plot_acti(acti_interval1)

#%% Extract one night of CGM data

i=0
in_bed = summed_data.iloc[i]['In Bed DateTime']
out_bed = summed_data.iloc[i]['Out Bed DateTime']

CGM_interval1 = extract_one_night(in_bed, out_bed, CGM_data)
plot_CGM(CGM_interval1)

#%% Plot of WASO and TIR

 layout = go.Layout(
        title="TIR against WASO"
        xaxis=dict(title="Time in range"),
        yaxis=dict(title="WASO"),
        showlegend=False
    )
    
    fig = go.Figure(data=[go.Scatter(x=tir, y=waso)], layout=layout)
    fig.show()
