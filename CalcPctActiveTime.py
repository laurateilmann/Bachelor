# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:06:30 2023

@author: LSKO0085
"""

import numpy as np
from datetime import timedelta


def CalcPctActiveTime(data):
    """
    Calculate percentage of active CGM time. 
    This function assumes that the CGM value measured at time point i has been
    constant since time point i-1.

    """
    
    TotalTime = timedelta(minutes=0)
    ActiveTime = timedelta(minutes=0)
    
    for i in range(1,len(data)):
        
        dt = data.loc[i,'DateTime']-data.loc[i-1,'DateTime']
        
        TotalTime += dt
        
        if not np.isnan(data.loc[i,'CGM']):
            ActiveTime += dt
    
    if TotalTime > timedelta(minutes=0):
        PctActiveTime = ActiveTime/TotalTime*100
    
    
    return PctActiveTime, TotalTime