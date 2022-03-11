# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 11:44:46 2022

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

leastquare_path = 'C:\\Users\\LuizF\\Google Drive\\My Drive\\'\
    'Python\\code-master\\NumericalApplications\\'
    
sys.path.insert(1, leastquare_path)

from LeastSquare import *


path_main = 'G:\\My Drive\\Python\\doctorate-master'\
    '\\AtmospherePhysics\\Database\\'
    
infile = path_main + 'Magnetometer15012022\\'

tm1 = datetime.datetime(2022, 1, 15, 13, 0)
tm2 = datetime.datetime(2022, 1, 15, 17, 0)

component = 'H(nT)'
names, acc, lat, lon = sites_infos()

#period average (see LombScargle Analysis)
period = 0.5503718606933984

fig, axs = plt.subplots(figsize = (6, 10), 
                       sharex = True, 
                       nrows = len(acc))

plt.subplots_adjust(hspace = 0)

phase_result = {}

for ax, num in zip(axs.flat, range(len(acc))):
    
    # Use the sites locations (latitudes sorted) 
    # for get the acromics in crescent order
    filename = f'{acc[num]}15jan.22m'
    
    df = setting_dataframe(infile, filename, 
                           component = component)
    
    df = df.loc[(df.index > tm1) & (df.index < tm2), :]
    
    y = df['dtrend'].values
    t = df['time'].values
    
    ax.plot(t, y, lw = 1, color = 'k', label = 'Data (dtrend)')
    
    remove_lines(ax, acc, num)
    
    fit = least_square(t, y, period = period)
    
    phase_result[names[num]] = fit.phase
    
    ax.plot(t, fit.get_values, label = 'Wave reconstructed')
    
    #Put the name of location
    ax.text(0.03, 0.8, names[num], 
            transform = ax.transAxes)
    
    limit = 10
    ax.set(ylim = [-limit, limit], xlabel = 'Local time')
    
if component == 'H(nT)':
    ylabel = 'Horizontal'
elif component == 'Z(nT)':
    ylabel = 'Vertical'


ax.legend(loc = 'center', bbox_to_anchor=(0.5, 8.2), ncol = 2)

fig.text(0.01, 0.5, f'{ylabel} component (nT)', va='center', 
             rotation='vertical', fontsize = 12)   

fig.suptitle(('Least squares analysis \n Horizontal component - ' + 
              f'{tm1.strftime("%H:%M")}-{tm2.strftime("%H:%M")}'), 
             y = 0.97)

plt.rcParams.update({'font.size': 12})    

NameToSave =  f'{ylabel}{tm1.strftime("%d%m%Y")}LeastSquareAnalysis.png'

print(phase_result)
#save_plot(infile, NameToSave = NameToSave)

plt.show()