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
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def plot_LombScargle(ax, t, y, 
                     minimum_period = 0.3, 
                     maximum_period = 2):    
        
    #compute the periodogram and false alarm probability 
    ls = LombScargle(t, y, normalization='standard')
    fap = ls.false_alarm_level([0.5]) #95% of significace
    #Compute 
    frequency, power = ls.autopower(minimum_frequency = (1 / maximum_period), 
                                    maximum_frequency = (1 / minimum_period), 
                                    samples_per_peak = 100)
    
    #plot the power in function of period
    period = (1 / frequency)
    
    if ax:
        ax.plot(period, power, lw = 1, color = 'black') 
        
        #Plot false alarm probability
        ax.axhline(fap, linestyle = ':', color = 'black', 
                   label = 'Confidence 95%')
        
    return period, power

    
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
    
    
    if remove:
        sites = np.delete(sites, remove, axis = 0)
        
    sites = sites[::-1]
    
    names = sites[:, 0]
    acc = sites[:, 1]
    lat = sites[:, 2]
    lon = sites[:, 3]
    
    return names, acc, lat, lon

def save_plot(infile, NameToSave):

    path_to_save = infile + 'Figures\\'
    
    plt.savefig(path_to_save + NameToSave, 
                dpi = 1000, bbox_inches="tight")
    
def get_datetime():
    
    folder = 'Magnetometer15012022'

    fmtdate = folder.replace('Magnetometer', '')
    
    day = int(fmtdate[:2])
    mon = int(fmtdate[2:4])
    yer = int(fmtdate[4:])
    
    
    
    # Select area for to shade (analysis)
    tm1 = datetime.datetime(2022, 1, 15, 13, 0)
    tm2 = datetime.datetime(2022, 1, 15, 17, 0)
    
def concat_mag_files(infile, folder):        
    
    new_infile = f'{infile}{folder}\\'
    _, _, files = next(os.walk(new_infile))
    
    join = [setting_dataframe(new_infile, filename) for 
            filename in files[::-1]]
    
    return pd.concat(join)

def setting_axes(ax, color = 'red', position = 'left'):
    ax.yaxis.label.set_color(color)
    ax.spines[position].set_color(color)
    ax.tick_params(axis = 'y', colors = color)
