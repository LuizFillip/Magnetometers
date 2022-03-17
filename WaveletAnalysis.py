# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:23:32 2022

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

tm1 = datetime.datetime(2022, 1, 15, 13, 0)
tm2 = datetime.datetime(2022, 1, 15, 19, 0)

component = 'H(nT)'
transform = 'amplitude'


nrows = 4
ncols = 2
fig, ax = plt.subplots(figsize = (12, 10), sharex = True, sharey = True,
                       nrows = nrows, ncols = ncols)
plt.subplots_adjust(hspace = 0, wspace = 0)

bars = []

for x in range(nrows):
    for y in range(ncols):
        
        num = ((x + 1) * (y + 1)) - 1
        filename = f'{acc[num]}15jan.22m'
    
        # Read the files
        df = setting_dataframe(infile + folder, 
                           filename, component = component)
        
        im = plot_Wavelet(df, ax[x, y], transform = transform)
        
        #bars.append(im.get_array())
        
        ax[x, y].text(0.03, 0.89, names[num], transform = ax[x, y].transAxes)
        
        delta = datetime.timedelta(minutes = 30)
        
        ax[x, y].set(ylim = [0, 1.3], 
                    xlim = [df.index[0] - delta, df.index[-1] + delta],
                     yticks = np.arange(0, 1.2, 0.2))
        
        ax[x, y].xaxis.set_major_formatter(dates.DateFormatter('%H'))   
        ax[x, y].xaxis.set_major_locator(dates.HourLocator(interval = 2))
        
        if y == 0:
            ax[x, y].spines['right'].set_visible(False)
            if x == 0: 
                ax[x, y].spines['bottom'].set_visible(False)
            elif x == (nrows - 1):
                ax[x, y].spines['top'].set_visible(False)   
            else:
                ax[x, y].spines['top'].set_visible(False)   
                ax[x, y].spines['bottom'].set_visible(False)  
                
        else:
            ax[x, y].spines['left'].set_visible(False)
            if x == 0: 
                ax[x, y].spines['bottom'].set_visible(False)
                ax[x, y].axes.yaxis.set_visible(False)
            elif x == (nrows - 1):
                ax[x, y].spines['top'].set_visible(False)   
                ax[x, y].axes.yaxis.set_visible(False)
            else:
                ax[x, y].spines['top'].set_visible(False)   
                ax[x, y].spines['bottom'].set_visible(False)  
                ax[x, y].axes.yaxis.set_visible(False)
            
        
fontsize = 14

import matplotlib as mpl


cax, kw = mpl.colorbar.make_axes([axes for axes in ax.flat])

if transform == 'power':    
    vmin, vmax = 0, 1
else:
    vmin, vmax = -1, 1
    
cbar = fig.colorbar(im, cax=cax, **kw, 
                    ticks = np.arange(vmin, vmax + 0.1, 0.1))

cbar.set_label(f'{transform.title()} Spectral Density (normalized)')

fig.text(0.07, 0.5, 'Period (hours)', va='center', 
             rotation='vertical', fontsize = fontsize)   

fig.text(0.4, 0.08, 'Time (hours)', va='center', 
             rotation='horizontal', fontsize = fontsize)   


fig.suptitle(f'Wavelet Analysis - {transform.title()} Spectral - {tm2.date()}', 
             y = 0.92)

plt.rcParams.update({'font.size': fontsize})    


NameToSave = f'{transform.title()}{tm1.strftime("%d%m%Y")}WaveletNormalized.png'
#save_plot(NameToSave, dpi = 100)
plt.show()            

