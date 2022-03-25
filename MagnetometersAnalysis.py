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
from pylab import *
import matplotlib.ticker as ticker
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
    columns = {'YYYY': 'year', 'MM': 'month', 'DD': 'day', 
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

def all_rows_cols(df):
    with pd.option_context('display.max_rows', None, 
                           'display.max_columns', None): 
        print(df)


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




def plot_Wavelet(df, ax = None, 
                 transform = 'power', 
                 maximum_period = 1.1, 
                 minimum_period = 0.1):
    
    '''
    Compute and plot wavelet analysis
    software from Torrence and Compo 1998. 
    
    '''
    
    wavelet_path = 'C:\\Users\\LuizF\\Google Drive\\My Drive\\'\
    'Python\\code-master\\wavelets-master\\wave_python\\'
    
    sys.path.insert(1, wavelet_path)
    from waveletFunctions import wave_signif, wavelet
    
    dt = 0.016 # sampling time
    sst = df['dtrend'].values
    time = df['time'].values
    pad = 1
    variance = np.std(sst, ddof=1) ** 2
    mother = 'MORLET'
    lag1 = 0.01
    s0 = 2 * dt  
    
    n  = len(sst)
    if 0:
        variance = 1.0
        sst = sst / np.std(sst, ddof=1)
     
    #wavelet transform
    wave, period, scale, coi = wavelet(sst, dt = dt, pad = pad, s0 = s0)
    
    transform = transform.lower()
    
    # Chooice between
    if transform == 'power':
        # Compute the power spectrum
        power = (np.abs(wave))**2  
        
    elif transform == 'phase':
        # Compute the phase
        power = np.arctan2(np.imag(wave), np.real(wave)) 
    else:
        # Compute the amplitude
        power = np.real(wave)
        
    # Filter the periods
    condition = ((period >= minimum_period) & (period <= maximum_period))
        
    ind = np.where(condition)
    new_period = period[condition]
    new_power = power[ind, :][0]
    new_power = new_power / np.max(new_power)
 
    time = df.index
    if ax:
    
        levels = MaxNLocator(nbins=80).tick_values(new_power.min(), 
                                                   new_power.max())
        
        im = ax.contourf(time, new_period, new_power, 
                         levels = levels, cmap = 'jet')
        return im
    
    return time, new_period, new_power, new_sig95
    
def remove_lines(ax, acc, num):
    
    '''
    Remove inferior and superior lines (spines) from the subplots
    with the exception the firt (must have the top spine)
    and the last one, must have the bottom, only. 
    '''
    if num == 0:    
        ax.spines['bottom'].set_visible(False)       
    elif num == (len(acc) - 1):    
        ax.spines['top'].set_visible(False)
    else:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        
def sites_infos(remove = (3, 5)):
    
    '''
    Array with informations about the EMBRACE magnetormetors 
    sites. This array content the name of the city, acromic
    
    '''

    sites = np.array([['Rio Grande', 'rga', -53.78, -67.70],
                    ['São Martinho da Serra', 'sms', -29.53,-53.85], 
                    ['Tucumán', 'tcm', -26.56, -64.88], 
                    ['São José Dos Campos', 'sjc', -23.19, -45.89], 
                    ['Vassouras', 'vss', -22.41, -43.66],
                    ['Jataí', 'jat', -17.88, -51.72], 
                    ['Cuiabá', 'cba', -15.60, -56.10], 
                    ['Araguatins', 'ara', -5.65, -48.12], 
                    ['Eusébio', 'eus',  -3.89, -38.45], 
                    ['São Luis', 'slz', -2.53, -44.30]])
      
    if remove is not None:
        sites = np.delete(sites, remove, axis = 0)
        
    sites = sites[::-1] #inverse order from high latitudes to lower
    
    #get informations
    names = sites[:, 0]
    acronym = sites[:, 1]
    latitudes = pd.to_numeric(sites[:, 2])
    longitudes = pd.to_numeric(sites[:, 3])
    
    return names, acronym, latitudes, longitudes

def save_plot(NameToSave, dpi = 100):
    
    '''
    Save the figures in 'figures' folder (results)
    '''

    path_to_save = 'C:\\Users\\LuizF\\Google Drive\\My Drive\\'\
        'Python\\doctorate-master\\MagnetometerAnalysis\\Figures\\'
    
    plt.savefig(path_to_save + NameToSave, 
                dpi = dpi, bbox_inches="tight")
    
def datetime_from_foldername_(folder = 'Magnetometer15012022'):
    
    fmtdate = folder.replace('Magnetometer', '')
    
    day = int(fmtdate[:2])
    month = int(fmtdate[2:4])
    year = int(fmtdate[4:])
    
    # Select area for to shade (analysis)
    tm1 = datetime.datetime(year, month, day, 13, 0)
    tm2 = datetime.datetime(year, month, day, 17, 0)
    
def concat_mag_files(infile, folder):        
    
    '''
    Apply setting dataframe, for data organize, 
    
    '''
    
    new_infile = f'{infile}{folder}\\'
    _, _, files = next(os.walk(new_infile))
    
    join = [setting_dataframe(new_infile, filename) for 
            filename in files[::-1]]
    
    return pd.concat(join)

def change_color_axes(ax, color = 'red', position = 'left'):
    '''
    Change the color of ticks and spines on the axes,
    for the same color of the line
    '''
    ax.yaxis.label.set_color(color)
    ax.spines[position].set_color(color)
    ax.tick_params(axis = 'y', colors = color)
