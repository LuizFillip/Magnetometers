# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 19:55:27 2022

@author: LuizF
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as dates
import os

from astropy.timeseries import LombScargle


def setting_dataframe(infile, filename, component = 'H(nT)', N = 10):
    """
    Function for to organize magnetormeters data from EMBRACE (INPE).
    Here, returns dTrend array from the component desired with the 
    running average. Moreover, it creates more two columns for the time: 
    One in the datetime format (for dataframe index) and other it is
    running time (float array), the last can be used in numerical 
    analysis (Lomb Scargle, least squares, wavelets and others). 
    """
    
    #read csv file 
    df = pd.read_csv(infile + filename, 
                     header = 1, delim_whitespace = True)
    #dictionary for rename columns
    columns = {'YYYY': 'year',
               'MM': 'month', 'DD': 'day', 
               'HH':'hour', 'MM.1':'minute'}

    df.rename(columns = columns, inplace = True)

    df.index = pd.to_datetime(df[['day', 'month', 'year', 'hour', 
                                  'minute']],infer_datetime_format = True)
    
    df['time'] = df['hour'] + (df['minute'] / 60)
    
    df = df.drop(columns = list(columns.values()))
    
    df.index = pd.to_datetime(df.index)
    
    if component:
        
        df['dtrend'] = (df[component] - 
                        df[component].rolling(window = N).mean())
        df = df.dropna()
    
    df.index = pd.to_datetime(df.index) 
    return df


def running_mean(x, N):
    
    "Rununing average for array. N parameter it is a window (number of elements)"
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)




def plot_LombScargle(t, y, ax = None, 
                     minimum_period = 0.3, 
                     maximum_period = 2):    
    
    '''
    Compute and plot the Lomb-Scargle periodogram (Astropy library)
    '''
        
    #compute the periodogram and false alarm probability 
    ls = LombScargle(t, y, normalization='standard')
    #95% of significance level
    fap = ls.false_alarm_level([0.5]) 
    #Compute 
    frequency, power = ls.autopower(minimum_frequency = (1 / maximum_period), 
                                    maximum_frequency = (1 / minimum_period), 
                                    samples_per_peak = 100)
    
    # Compute the period (inverse of frequency)
    period = (1 / frequency)
    
    if ax:
        ax.plot(period, power, lw = 1, color = 'black') 
        
        #Plot false alarm probability
        ax.axhline(fap, linestyle = ':', color = 'black', 
                   label = 'Confidence 95%')
        
    return period, power

        
        