# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 20:48:33 2022

@author: LuizF
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as dates
import datetime
import os.path
import sys
import os 

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from MagnetometersAnalysis import *


infile = 'G:\\My Drive\\Python\\doctorate-master\\'\
        'AtmospherePhysics\\Database\\'
        
    

# Get data from São Luis and Rio Grande
rga = concat_mag_files(infile, 'RGA')
slz = concat_mag_files(infile, 'SLZ')

fontsize = 14

fig, axs = plt.subplots(figsize = (12, 6), 
                       nrows = 2, sharex = True)
plt.subplots_adjust(hspace = 0)

names = ['São Luis', 'Rio Grande']
data = [slz, rga]

for ax, num in zip(axs.flat, range(2)):
    
  
    data[num]['H(nT)'].plot(ax = ax, lw = 1, color = 'k')
    
    ax1 = ax.twinx()
    
    # Plot vertical component in the right axes
    vertical, = ax1.plot(data[num]['Z(nT)'], lw = 1)
    
    setting_axes(ax1, color = vertical.get_color(), position = 'right')
    
    #print(vertical.get_color())

    locator = dates.MonthLocator(bymonthday=(1, 15))
    formatter = dates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.text(0.01, 0.1, names[num], fontsize = fontsize,
               transform = ax.transAxes)

    if num == 0: 
        ax.spines['bottom'].set_visible(False)       
        ax1.spines['bottom'].set_visible(False)       
    else:
        ax.spines['top'].set_visible(False)
        ax1.spines['top'].set_visible(False)


    ax.set(xlabel = 'Days', xlim = [data[num].index[0], 
                                    data[num].index[-1]])
    
    dt1 = datetime.datetime(2022, 1, 15, 0)
    dt2 = datetime.datetime(2022, 1, 16, 0)
    
    ax.axvspan(dt1, dt2, color='lightgrey', alpha = 0.4, lw=0)
    
    fig.autofmt_xdate(rotation = 0, ha = 'center')



fig.text(0.04, 0.5, f'Horizontal component (nT)', va='center', 
             rotation='vertical', fontsize = fontsize)   

fig.text(0.98, 0.5, f'Vertical component (nT)', va='center', 
             rotation='vertical', fontsize = fontsize, 
             color = vertical.get_color()) 

plt.rcParams.update({'font.size': fontsize})    

plt.suptitle('EMBRACE Magnetometers \n Comparation between São Luis and Rio Grande', 
             y = 0.99)

NameToSave = 'SaoLuis_RioGrande_Comparation.png'
path_to_save = infile + 'Figures\\'

plt.savefig(path_to_save + NameToSave, dpi = 1000)


plt.show()
