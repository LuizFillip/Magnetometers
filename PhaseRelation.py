# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:31:28 2022

@author: LuizF

Python has methods for finding a relationship between 
data-points and to draw a line of linear regression.
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
from scipy import stats


phase = {'São Luis': 2.4840810675436993, 
         'Eusébio': 2.64309755509854, 
         'Araguatins': 2.895963505966484, 
         'Cuiabá': 2.4469029094392423, 
         'Vassouras': 2.568248484768612, 
         'Tucumán': 2.3407382800854384, 
         'São Martinho da Serra': 2.1886168408557714, 
         'Rio Grande': 2.322724534575036}

names, acc, lat, lon = sites_infos()
phases = np.array(list(phase.values()))
latitudes = np.array(lat, dtype = 'float')
longitudes = np.array(lon, dtype = 'float')

ylabel = 'Latitudes'
ylabel = 'Longitudes'

if ylabel == 'Longitudes':
    parameter = longitudes
else:
    parameter = latitudes

fig, ax = plt.subplots(figsize = (10, 5))

for phase, name, lat in zip(phases, names, parameter):
    ax.plot(phase, lat, label = name, 
            marker = 'o', markersize = 8)

slope, intercept, r, p, std_err = stats.linregress(phases, parameter)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, phases))

ax.plot(phases, mymodel, color = 'k')


ax.set(ylabel = f'{ylabel} (°)', xlabel = 'Phases (hours)', 
       title = f'Relation between {ylabel} and phases')

infos = (f'Slope: {round(slope, 2)}\nIntercept: {round(intercept, 2)}\n' + 
         f'Coefficient of correlation {round(r, 2)}\nError $\pm${round(std_err, 2)}')

fontsize = 14
ax.text(0.61, 0.1, infos, transform = ax.transAxes, fontsize = fontsize)

ax.legend(bbox_to_anchor=(1.39, 0.85), title = 'Sites')

plt.rcParams.update({'font.size': fontsize})    


NameToSave = f'Relation{ylabel}Phases15012022.png'



infile = 'G:\\My Drive\\Python\\doctorate-master\\'\
        'AtmospherePhysics\\Database\\'
        
    
save_plot(infile, NameToSave = NameToSave)

plt.show()