# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 17:24:15 2023

@author: MGRO0154 & LTEI0004

Plot histograms of residuals of Model_WN, Model_WH, and Model_SE
"""

#%% Import packages

import pandas as pd
import matplotlib.pylab as plt
import os

#%% Pre settings 

# Close all figures
plt.close('all')

# Base directory
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data\Residuals"

# Output directory
out_dir = r"H:\GitHub\Bachelor\Plots"

#%% WASO nightly - Model_WN

# Import data
file_path = os.path.join(base_dir, 'residuals_Model_WN.csv')
residuals_waso =  pd.read_csv(file_path)

# Histogram of residuals
plt.figure(figsize=(12,10.5))
plt.hist(residuals_waso, bins=20)
plt.title("Histogram of WASO residuals (nightly)", fontname="Times New Roman", fontsize=47)
plt.xlabel("Residuals", fontsize=45, family='Times New Roman', labelpad=20)
plt.ylabel("Frequency", fontsize=45, family='Times New Roman', labelpad=20)
plt.xticks(fontsize=40, family='Times New Roman')
plt.yticks(fontsize=40, family='Times New Roman')
plt.tight_layout()
plt.show()

# Save figure
out_path = os.path.join(out_dir, 'Model_WN_residuals.png')
plt.savefig(out_path)

#%% WASO hourly - Model_WH

# Import data
file_path = os.path.join(base_dir, 'residuals_Model_WH.csv')
residuals_waso_h =  pd.read_csv(file_path)

# Histogram of residuals
plt.figure(figsize=(12,10.5))
plt.hist(residuals_waso_h, bins=20)
plt.title("Histogram of WASO residuals (hourly)", fontname="Times New Roman", fontsize=47)
plt.xlabel("Residuals", fontsize=45, family='Times New Roman', labelpad=20)
plt.ylabel("Frequency", fontsize=45, family='Times New Roman', labelpad=20)
plt.xticks(fontsize=40, family='Times New Roman')
plt.yticks(fontsize=40, family='Times New Roman')
plt.tight_layout()
plt.show()

# Save figure
out_path = os.path.join(out_dir, 'Model_WH_residuals.png')
plt.savefig(out_path)

#%% Efficiency - Model_SE

# Import data
file_path = os.path.join(base_dir, 'residuals_Model_SE.csv')
residuals_eff =  pd.read_csv(file_path)

# Histogram of residuals
plt.figure(figsize=(12,10.5))
plt.hist(residuals_eff, bins=20)
plt.title("Histogram of Efficiency residuals", fontname="Times New Roman", fontsize=55)
plt.xlabel("Residuals", fontsize=52, family='Times New Roman', labelpad=20)
plt.ylabel("Frequency", fontsize=52, family='Times New Roman', labelpad=20)
plt.xticks(fontsize=45, family='Times New Roman')
plt.yticks(fontsize=45, family='Times New Roman')
plt.tight_layout()
plt.show()

# Save figure
out_path = os.path.join(out_dir, 'Model_SE_residuals.png')
plt.savefig(out_path)

