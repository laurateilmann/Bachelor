# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 17:24:15 2023

@author: MGRO0154
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sklearn.linear_model as lm
import matplotlib.pylab as plt
from scipy.stats import zscore
from sklearn.preprocessing import StandardScaler
from sklearn import model_selection, linear_model
import os

# Base directory
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\Concatenated data\Residuals"

#%% WASO

# Import data
file_path = os.path.join(base_dir, 'residuals_WASO_CV.csv')
residuals_waso =  pd.read_csv(file_path)

# Histogram of residuals
plt.figure(figsize=(8,7))
plt.hist(residuals_waso, bins=20)
plt.title("Residuals for WASO against CV (nightly)", fontname="Times New Roman", fontsize=30)
plt.xlabel("Residuals", fontsize=28, family='Times New Roman')
plt.ylabel("Frequency", fontsize=28, family='Times New Roman')
plt.xticks(fontsize=26, family='Times New Roman')
plt.yticks(fontsize=26, family='Times New Roman')
plt.tight_layout()
plt.show()

# Save figure
out_dir = r"H:\GitHub\Bachelor\Plots"
out_path = os.path.join(out_dir, 'WASO_CV_residuals.png')
plt.savefig(out_path)

#%% Efficiency

# Import data
file_path = os.path.join(base_dir, 'residuals_Efficiency_CV.csv')
residuals_eff =  pd.read_csv(file_path)

# Histogram of residuals
plt.figure(figsize=(8,7))
plt.hist(residuals_eff, bins=20)
plt.title("Residuals for Effciency against CV", fontname="Times New Roman", fontsize=30)
plt.xlabel("Residuals", fontsize=28, family='Times New Roman')
plt.ylabel("Frequency", fontsize=28, family='Times New Roman')
plt.xticks(fontsize=26, family='Times New Roman')
plt.yticks(fontsize=26, family='Times New Roman')
plt.tight_layout()
plt.show()

# Save figure
out_dir = r"H:\GitHub\Bachelor\Plots"
out_path = os.path.join(out_dir, 'Efficiency_CV_residuals.png')
plt.savefig(out_path)

