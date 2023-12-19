# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:37:15 2023

@author: MGRO0154
"""



#%% Import packages
import pandas as pd
import os
from CalcPctActiveTime import *
import numpy as np

#%%
studies = ["MindYourDiabetes", "Sleep-1-child_2023_Cecilie", "Validationstudy_2020_2021_Cecilie"]

# Base directory/path
base_dir = os.path.join(r"L:\LovbeskyttetMapper01\StenoSleepQCGM")
  
   
#%%  
    
active_time = []
total_time = []
    
for study in studies:
    # Base directory/path
    study_dir = os.path.join(base_dir, study)
    
    # List of families
    families = [folder for folder in os.listdir(study_dir) if os.path.isdir(os.path.join(study_dir, folder))]
    
    # List of sessions
    if study == "Validationstudy_2020_2021_Cecilie" or study == "Sleep-1-child_2023_Cecilie":
        sessions = [None]
    else:
        folder_path = os.path.join(study_dir,families[0])
        sessions = [folder for folder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder))]
    
    # Loop through each family
    for family in families:
        # Loop through each session for the family
        for session in sessions:
            # Create path
            if session==None:
                cgm_dir = os.path.join(study_dir, family)
            else:
                cgm_dir = os.path.join(study_dir, family, session)
                
            cgm_path = os.path.join(cgm_dir, "cgm_data_processed.csv")
            
            if os.path.exists(cgm_path):
                cgm = pd.read_csv(cgm_path, parse_dates=[0, 1], dayfirst=True)
            else:
                print(f"Either/both epoch and CGM data file does not exist in {family}/{session}. Skipping...")
                continue
      
            cgm['CGM'] = cgm['CGM'].astype(float)
            
            PctActiveTime, TotalTime = CalcPctActiveTime(cgm)
            active_time.append(PctActiveTime)
            total_time.append(TotalTime)
            
            print(f"Processed {study}/{family}/{session}")

mu_active = np.mean(active_time)
min_active = np.min(active_time)        
max_active = np.max(active_time)

print(f"Mean: {mu_active}, min: {min_active}, max: {max_active}")       
            
             