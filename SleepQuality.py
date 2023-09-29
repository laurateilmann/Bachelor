# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 09:44:02 2023

@author: ltei0004
"""

#%% Sleep Quality definitions

#Very good sleeper:
#latency < 15 min
#Efficiency > 90%
#WASO < 5 min

#Fairly good sleeper:
#latency = 15-20 min
#Efficiency = 85-90%
#WASO = 5-15 min

#Fairly bad sleeper:
#latency = 21-31 min
#Efficiency = 80-84%
#WASO = 16-30 min

#Very bad sleeper:
#latency > 31 min
#Efficiency < 80%
#WASO > 31 min


#%% Import packages
import pandas as pd
from datetime import datetime
from ExtractIntervals import extract_one_night
import numpy as np
import os
from ActiFeaturesFunc import *
import csv

#%% Set the base directory for the current family and session
base_dir = r"L:\LovbeskyttetMapper01\StenoSleepQCGM\MindYourDiabetes"

# List of families
families = ["Fam01", "Fam03", "Fam05", "Fam06", "Fam07", "Fam09"]

# List of sessions for each family
sessions = ["Baseline", "Second", "Third"]
     
   
#%% Define the sleep quality criteria
criteria = {
    "Very good sleeper": {"latency": (0, 15), "efficiency": (90, 100), "WASO": (0, 5)},
    "Fairly good sleeper": {"latency": (15, 20), "efficiency": (85, 90), "WASO": (5, 15)},
    "Fairly bad sleeper": {"latency": (21, 31), "efficiency": (80, 84), "WASO": (16, 30)},
    "Very bad sleeper": {"latency": (31, np.inf), "efficiency": (0, 80), "WASO": (31, np.inf)},
}


# Create a dictionary to store the sleep quality characterization for each family and session
sleep_quality = {}

# Iterate through each family and session
for family in families:
    for session in sessions:
        # Construct the file path for the CSV data for the current family and session
        csv_file = os.path.join(base_dir, family, session, "sum_fam_processed.csv")  # Adjust the file path as needed

        # Check if the CSV file exists
        if os.path.isfile(csv_file):
            # Initialize the sleep quality category as None
            sleep_category = None

            # Read data from the CSV file
            with open(csv_file, mode="r") as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row, assuming it contains column names
                for row in csv_reader:
                    latency = float(row[1])  # Assuming latency is in the second column
                    efficiency = float(row[3])  # Assuming efficiency is in the fourth column
                    WASO = float(row[6])  # Assuming WASO is in the seventh column

                    # Iterate through the defined sleep quality criteria
                    for category, criteria_values in criteria.items():
                        latency_range = criteria_values["latency"]
                        efficiency_range = criteria_values["efficiency"]
                        WASO_range = criteria_values["WASO"]

                        # Check if the current metrics fall within the criteria range
                        if (
                            (latency_range[0] <= latency <= latency_range[1]) and
                            (efficiency_range[0] <= efficiency <= efficiency_range[1]) and
                            (WASO_range[0] <= WASO <= WASO_range[1])
                        ):
                            sleep_category = category  # Set the sleep category if criteria are met
                            break  # Exit the loop once a category is assigned
                        

            # Store the sleep quality category for the current family and session
            sleep_quality[(family, session)] = sleep_category

# Print the sleep quality characterization for each family and session
for (family, session), category in sleep_quality.items():
    print(f"Family {family}, Session {session}: {category}")
    
#%%