# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 13:03:10 2023

@author: LSKO0085
"""

import pandas as pd
import os
import numpy as np
import csv
from datetime import datetime, date

from MarkMissingData import MarkMissingData


def PrepareLibreviewData(file):
    
    data = []
    
    with open(file, mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            #row = str(row).replace('"','').replace('[','').replace(']','')
            row = str(row).split(",")
            
            data.append(row)
            
            line_count += 1 

    # Delete file header rows if present
    if "Enhed" not in data[0][0]:
        del data[:2]
    
    
    #datetime_raw = [datetime.strptime(line[2].replace('"', '').replace(" '","").replace("'",""), '%d-%m-%Y %H:%M') for line in data[1:]]
    datetime_raw = [line[2].replace('"', '').replace(" '","").replace("'","") for line in data[1:]]
    datetimes = []
    for i in range(len(datetime_raw)):
        if datetime_raw[i] == '' or int(datetime_raw[i][6:10])<1900:
            datetimes.append(datetime.strptime('01-01-1800 12:00','%d-%m-%Y %H:%M'))
        else:
            datetimes.append(datetime.strptime(datetime_raw[i],'%d-%m-%Y %H:%M'))
        
    
    d1 = [line[4].replace('"', '').replace(" ","").replace("'","")  for line in data[1:]]
    d2 = [line[5].replace('"', '').replace(" ","").replace("'","")  for line in data[1:]]

    CGMdata = []
    for i in range(len(d1)):
        if d1[i]=='':
            CGMdata.append(float("Nan"))
        else:
            CGMdata.append(float(d1[i] + "." + d2[i]))
            
    Dataframe = pd.DataFrame({'DateTime':datetimes, 'CGM':CGMdata})
    Dataframe.loc[:,'DateTime'] = pd.to_datetime(Dataframe.loc[:,'DateTime'])
    

    # Sort the data
    Dataframe.dropna(inplace=True)
    Dataframe.sort_values(by='DateTime',ascending=True,inplace=True)
    Dataframe.reset_index(inplace=True, drop=True)  

    Dataframe = MarkMissingData(Dataframe, dt=15)

    return Dataframe



# =============================================================================
#     first_line = pd.read_csv(file, low_memory = False, nrows = 1)
#     
#     columns = ['Tidsstempel', 'Glukosehistorik mmol/L']
#     
#     if first_line.columns[0] == "Enhed":
#         data = pd.read_csv(file, low_memory = False, nrows = 20)
#     else:
#         data = pd.read_csv(file, low_memory = False, skiprows = 2, nrows = 20)
# =============================================================================
   