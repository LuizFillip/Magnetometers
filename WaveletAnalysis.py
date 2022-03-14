# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 23:04:33 2022

@author: LuizF
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

component = 'H(nT)'

ncols = 2

fig, axs = plt.subplots(figsize = (12, 10), 
                        sharex= True, sharey=(True),  
                        nrows = 4, ncols = ncols)

plt.subplots_adjust(hspace = 0, wspace = 0)

transform = 'power'


for ax, num in zip(axs.flat, range(len(acc))):
    print(num)
    
    filename = f'{acc[num]}15jan.22m'
    
    # Read the files
    df = setting_dataframe(infile + folder, 
                       filename, component = component)
    
    im = plot_Wavelet(ax, df, transform = transform)

    ax.text(0.03, 0.9, names[num], transform = ax.transAxes)
    
    delta = datetime.timedelta(minutes = 30)
    ax.set(ylim = [-0.1, 1.2], xlim = [df.index[0] - delta, df.index[-1] + delta],
           yticks = np.arange(0, 1.3, 0.2))
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))   
    ax.xaxis.set_major_locator(dates.HourLocator(interval = 2))


#cbar_ax = fig.add_axes([0.91, 0.15, 0.03, 0.73])
#fig.colorbar(im, cax = cbar_ax, ticklocation='right')

fontsize = 14

fig.text(0.07, 0.5, 'Period (hours)', va='center', 
             rotation='vertical', fontsize = fontsize)   

fig.text(0.47, 0.08, 'Time (hours)', va='center', 
             rotation='horizontal', fontsize = fontsize)   

fig.suptitle(f'Wavelet Analysis - Power Spectral - {tm2.date()}', 
             y = 0.90)

plt.rcParams.update({'font.size': fontsize})    

plt.show()
