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

        
        
        
class sites_embrace:
    
    '''
    Array with informations about the EMBRACE magnetormetors 
    sites. This array content the name of the city, acromic
    
    '''
    def __init__(self, filename = None):
        
        self.infos_ = np.array([['Rio Grande', 'rga', -53.78, -67.70],
                        ['São Martinho da Serra', 'sms', -29.53,-53.85], 
                        ['Tucumán', 'tcm', -26.56, -64.88], 
                        ['São José Dos Campos', 'sjc', -23.19, -45.89], 
                        ['Vassouras', 'vss', -22.41, -43.66],
                        ['Jataí', 'jat', -17.88, -51.72], 
                        ['Cuiabá', 'cba', -15.60, -56.10], 
                        ['Araguatins', 'ara', -5.65, -48.12], 
                        ['Eusébio', 'eus',  -3.89, -38.45], 
                        ['São Luis', 'slz', -2.53, -44.30],
                        ["Pilar", "pil", -31.7, -63.89],
                        ["Tatuoca", "ttb", -1.205, -48.51]])
    
    
      
        if filename is not None:
            self.acc = filename
           
            self.cond = self.infos_[(self.infos_[:, 1] == 
                                     self.acc[:3])][0]
        
    @property
    def infos(self):
        return self.cond
    
    @property
    def sites_names(self):
        return self.infos_[:, 0]
    @property
    def acronyms(self):
        return self.infos_[:, 1]
    @property
    def latitudes(self):
        return pd.to_numeric(self.infos_[:, 2])
    @property
    def longitudes(self):
        return pd.to_numeric(self.infos_[:, 3]) 

def save_plot(NameToSave, dpi = 100):
    
    '''
    Save the figures in 'figures' folder (results)
    '''

    path_to_save = 'C:\\Users\\LuizF\\Google Drive\\My Drive\\'\
        'Python\\doctorate-master\\MagnetometerAnalysis\\Figures\\'
    
    plt.savefig(path_to_save + NameToSave, 
                dpi = dpi, bbox_inches="tight")
    

    
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
