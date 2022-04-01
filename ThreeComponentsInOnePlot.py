# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 09:49:49 2022

@author: LuizF

Plot the Compint
"""

import os.path
import sys
import matplotlib.ticker as ticker


file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from MagnetometersAnalysis import *


infile = 'G:\\My Drive\\Python\\doctorate-master\\'\
        'MagnetometerAnalysis\\Database\\'
        
folder = 'Magnetometer15012022\\'

names, acc, lat, lon = sites_infos()

num = 0

filename = f'{acc[num]}15jan.22m'
    
df = setting_dataframe(infile + folder, filename)

fig, ax = plt.subplots(figsize = (12, 5))

def setting_axes(ax, color = 'red', position = 'left'):
    ax.yaxis.label.set_color(color)
    ax.spines[position].set_color(color)
    ax.tick_params(axis = 'y', colors = color)

############### First axes ############
#horizontal component
left_color = 'black'
ax.plot(df['H(nT)'], color = left_color, lw = 1, label = 'H')
setting_axes(ax, color = left_color, position = 'left')

ax.set(ylabel = 'Horizontal component (nT)')

############### Second axes ############
out_ax = ax.twinx()

out_ax.yaxis.set_ticks_position('left') 
out_ax.yaxis.set_label_position('left') 
out_ax.spines['left'].set_position(('outward', 73))

#setting the color
out_color = 'green'
out_ax.plot(df['Z(nT)'], color = out_color, lw = 1, label = "Z")
setting_axes(out_ax, color = out_color, position = 'left')
out_ax.set(ylabel = 'Vertical component (nT)')

############### Third axes ############

right_ax = ax.twinx()

right_color = 'red'
right_ax.plot(df['D(Deg)'], color = right_color, lw = 1, label = 'D')
setting_axes(right_ax, color = right_color, position = 'right')
right_ax.set(ylabel = 'Declination component (°)')

### Setting datetime on the bottom axes 
ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(dates.HourLocator(interval = 2))


#.legend(bbox_to_anchor=[1.02, 0.5],  loc='center', ncol=1)

ax.set(xlabel = 'Universal time (UT)')

date = df.index[0].date().strftime("%Y/%m/%d")

fig.suptitle(f"Geomagnetic Components HDZ - {names[num]}: {date}", 
             y = .92)

plt.rcParams.update({'font.size': 12})  

ax.grid(True, which ='both', axis = 'both')

plt.show()
