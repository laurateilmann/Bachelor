# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 15:06:07 2023

@author: MGRO0154
"""

import plotly.graph_objects as go
import plotly.io as io

def plot_acti_raw(raw_data):
    """
    Plots actigraph data from raw agd file imported using pyActigraphys package.

    Parameters
    ----------
    raw_data : RawAGD object of pyActigraphy.io.agd.agd module.

    Returns
    -------
    None.

    """
    layout = go.Layout(
        title="Actigraphy data",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Vector magnitude"),
        showlegend=False
    )
    
    fig = go.Figure(data=[go.Scatter(x=raw_data.data.index.astype(str), y=raw_data.data)], layout=layout)
    fig.show()
    
    return None

def plot_acti(data):
    """
    Plots actigraph data from exported csv-file.


    Parameters
    ----------
    data : Pandas dataframe with two columns, one with the timeindexes called
    'Timestamp' and one with the vector magnitude from the actigraphy data
    called 'Magnitude'.

    Returns
    -------
    None.

    """
    layout = go.Layout(
        title="Actigraphy data",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Vector magnitude"),
        showlegend=False
    )
    
    fig = go.Figure(data=[go.Scatter(x=data['DateTime'], y=data['Magnitude'])], layout=layout)
    fig.show()
    
    return None


def plot_CGM(CGMData):
    """
    Plots CGM data from processed csv file.

    Parameters
    ----------
    CGMdata : Pandas dataframe
        Nx2 dataframe with the two columns: one with times and dates of 
        measurements called 'DateTime' and one with blood glucose measurements
        called 'CGM'.

    Returns
    -------
    None.

    """
    
    layout = go.Layout(
    title="CGM data",
    xaxis=dict(title="Time"),
    yaxis=dict(title="Blood glucose [mmol/L]"),
    showlegend=False
    )

    fig = go.Figure(data=[go.Scatter(x=CGMData['DateTime'], y=CGMData['CGM'])], layout=layout)
    fig.show()


