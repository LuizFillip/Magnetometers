# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 19:26:59 2022

@author: LuizF
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
from astropy.timeseries import LombScargle

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from MagnetometersAnalysis import *



path_main = 'G:\\My Drive\\Python\\doctorate-master\\AtmospherePhysics\\Database\\'


infile = path_main + 'Magnetometer15012022\\'



tm1 = datetime.datetime(2022, 1, 15, 13, 0)
tm2 = datetime.datetime(2022, 1, 15, 17, 0)



N = 10
component = 'Z(nT)'
names, acc, lat, lon = sites_infos()
    


fig, axs = plt.subplots(figsize = (6, 10), 
                       sharex = True, 
                       nrows = len(acc))

plt.subplots_adjust(hspace = 0)

best_period = {}

for ax, num in zip(axs.flat, range(len(acc))):
    
    # Use the sites locations (latitudes sorted) 
    # for get the acromics in crescent order
    filename = f'{acc[num]}{day}jan.22m'
    
    df = setting_dataframe(infile, filename, 
                           component = component)
    
    df = df.loc[(df.index > tm1) & (df.index < tm2), :]

    y = df['dtrend'].values
    t = df['time'].values
    
    remove_lines(ax, acc, num)
    

    try:
        period, power = plot_LombScargle(ax, t, y, 
                             minimum_period = 0.1, 
                             maximum_period = 0.8)
        
        best_period[names[num]] = period[np.argmax(power)]
        ax.set(ylim = [0, 0.3], xlabel = 'Period (hours)')
    except:
        pass
    
    #Put the name of location
    ax.text(0.02, 0.7, names[num], transform = ax.transAxes)
    

avg_period = np.array(list(best_period.values())).mean()

print(avg_period)

for ax in axs.flat:    
    ax.axvline(x=avg_period, label = 'Best period', )

ax.legend(loc = 'center', bbox_to_anchor=(0.5, 8.2), ncol = 2)


if component == 'H(nT)':
    ylabel = 'Horizontal'
elif component == 'Z(nT)':
    ylabel = 'Vertical'


fig.suptitle((f'Lomb-Scargle Periodogram\n {ylabel} component -' + 
             f'{tm1.strftime("%H:%M")}-{tm2.strftime("%H:%M")}'), 
             y = 0.97) 

fig.text(0.01, 0.5, 'Power Density Spectral (normalized)', va='center', 
         rotation='vertical', fontsize = 12) 


plt.rcParams.update({'font.size': 12})    


NameToSave = f'{ylabel}{day}{mon}{yer}LombScargle.png'
path_to_save = path_main + 'Figures\\'


#plt.savefig(path_to_save + NameToSave, dpi = 1000, bbox_inches="tight")


plt.show()  
    

