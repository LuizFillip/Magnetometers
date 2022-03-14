# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:26:02 2022

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

infile = 'G:\\My Drive\\Python\\doctorate-master\\MagnetometerAnalysis\\Database\\'
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
                           filename)
    
    # Plot Subract from running average 
    df[component].plot(ax = ax, color = 'k', lw = 1, label = 'data')
    df[component].rolling(window = N).mean().plot(ax = ax,
                                                  label = f'running average - {N} min',
                                                  lw= 2, linestyle = ':')

    #Put the name of location
    ax.text(0.03, 0.8, names[num], 
            transform = ax.transAxes)
    
    remove_lines(ax, acc, num)
    
    ax.axvspan(tm1, tm2, color='lightgrey', alpha=0.4, lw=0)
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
    ax.xaxis.set_major_locator(dates.HourLocator(interval = 2))
    
    ax.set(xlabel = 'Time (hours)')
    
    
ax.legend(loc = 'center', bbox_to_anchor=(0.5, 10.3), ncol = 2)
if component == 'H(nT)':
    ylabel = 'Horizontal'
elif component == 'Z(nT)':
    ylabel = 'Vertical'
elif component == 'F(nT)':
    ylabel = 'Total'


fig.text(-0.01, 0.5, f'Horizontal component (nT)', va='center', 
             rotation='vertical', fontsize = fontsize)   

fig.suptitle(f'Hourly variation of\n horizontal component - {tm2.date()}', 
             y = 0.97)

plt.rcParams.update({'font.size': 12})    

NameToSave = f'{ylabel}Component{tm1.strftime("%d%m%Y")}AllSites.png'

save_plot(NameToSave, dpi = 100)
plt.show()  
    
