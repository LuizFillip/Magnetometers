# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 15:16:31 2022

@author: LuizF
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as dates
import datetime
import os.path
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from MagnetometersAnalysis import *


# Select area for to shade (analysis)
tm1 = datetime.datetime(2022, 1, 15, 13, 0)
tm2 = datetime.datetime(2022, 1, 15, 19, 0)


component = 'H(nT)'
limit = 12
N = 10


infile = 'G:\\My Drive\\Python\\doctorate-master\\'\
        'MagnetometerAnalysis\\Database\\'
folder = 'Magnetometer15012022\\'

#Get sites informations from array in the file
names, acc, lat, lon = sites_infos(remove = None)

fig, axs = plt.subplots(figsize = (6, 10), 
                       sharex = True, 
                       nrows = len(acc))

plt.subplots_adjust(hspace = 0)


for ax, num in zip(axs.flat, range(len(acc))):
    
    # Use the sites locations (latitudes sorted) 
    # for get the acromics in crescent order
    filename = f'\\{acc[num]}15jan.22m'
    
        
    # Read the files
    df = setting_dataframe(infile + folder, 
                           filename, 
                           component = component)
    
    # Setting limits
    ax.set(ylim = [-limit, limit], xlabel = 'Local time',
           xlim = [df.index[0], df.index[-1]])
    
    # Plot Subract from running average 
    df['dtrend'].plot(ax = ax, color = 'k', lw = 1)
    
    #Put the name of location
    ax.text(0.03, 0.8, names[num], 
            transform = ax.transAxes)
    

    if num == 0:    
        ax.spines['bottom'].set_visible(False)       
    elif num == (len(acc) - 1):    
        ax.spines['top'].set_visible(False)
    else:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
    
    
    ax.axvspan(tm1, tm2, color='lightgrey', alpha=0.4, lw=0)
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
    ax.xaxis.set_major_locator(dates.HourLocator(interval = 2))
    
if component == 'H(nT)':
    ylabel = 'Horizontal'
elif component == 'Z(nT)':
    ylabel = 'Vertical'
elif component == 'F(nT)':
    ylabel = 'Total'


fig.text(0.01, 0.5, f'{ylabel} component (nT)', va='center', 
             rotation='vertical', fontsize = 12)   

fig.suptitle(f'EMBRACE Magnetometers Network\n dTrend - {tm2.date()}', 
             y = 0.93)

plt.rcParams.update({'font.size': 12})    


NameToSave = f'{ylabel}{tm1.strftime("%d%m%Y")}dTrendAnalysis.png'

#save_plot(NameToSave, dpi = 100)
plt.show()
