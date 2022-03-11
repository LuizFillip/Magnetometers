# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 14:09:38 2022

@author: LuizF
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as dates

infile = 'G:\\My Drive\\Python\\doctorate-master\\AtmospherePhysics\\'\
    'Database\\'

filename = 'Dst_012022.txt'

df = pd.read_csv(infile + filename, delim_whitespace = True, header= 17)

df.index = pd.to_datetime(df['DATE'] + ' ' + df['TIME'], 
                          errors  = 'coerce')

df['DST'] = pd.to_numeric(df['DST'], errors='coerce')

start = pd.to_datetime('2022-01-15 00:00')
end = pd.to_datetime('2022-1-16 00:00')
month = 'January 2022'

delta = datetime.timedelta(days = 7)

df = df.loc[(df.index > (start - delta)) & (df.index < (end + delta)), 
            ['DST']]

fig, ax = plt.subplots(nrows = 2, figsize = (10, 8))

plt.subplots_adjust(hspace = 0.2)

def monthly_plot(ax, df, start, end):
    
    ax.axvspan(start, end, color='lightgrey', alpha=0.4, lw=0)
    
    ax.plot(df['DST'], color = 'k', lw = 1)
    
    ax.set(ylabel = 'Dst index (nT)', xlabel = 'days', 
           title = f'Disturbance Storm-Time (Dst) - {month}')
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%d'))
    ax.xaxis.set_major_locator(dates.DayLocator(interval = 1))
    
    ax.axhline(-50, color='black', linestyle=':', lw = 1)
    
    ax.text(.99, 0.32, 'High activity', ha='right', va='bottom', 
            transform=ax.transAxes, size = 14)
    
    
monthly_plot(ax[0], df)

df.loc[df.index.day == 15, :].plot(ax = ax[1], label = None,
                                   color = 'k', lw = 1)

ax[1].set(xlabel = 'hours', ylabel = 'Dst index (nT)')

plt.rcParams.update({'font.size': 12})    

NameToSave = f'DstIndex{month}.png'
path_to_save = infile + 'Figures\\'

plt.savefig(path_to_save + NameToSave, dpi = 1000)


plt.show()
