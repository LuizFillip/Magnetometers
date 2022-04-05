# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 19:26:59 2022

@author: LuizF
"""

from astropy.timeseries import LombScargle
import sys
import os
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from MagnetometersAnalysis import *


infile = 'G:\\My Drive\\Python\\doctorate-master\\MagnetometerAnalysis\\Database\\'

folder = 'Magnetometer15012022\\'

tm1 = datetime.datetime(2022, 1, 15, 13, 0)
tm2 = datetime.datetime(2022, 1, 15, 19, 0)

N = 10
component = 'H(nT)'
names, acc, lat, lon = sites_infos()
    
fig, axs = plt.subplots(figsize = (6, 10), 
                       sharex = True, 
                       nrows = len(acc))
plt.subplots_adjust(hspace = 0)

best_period = {}

for ax, num in zip(axs.flat, range(len(acc))):
    
    # Use the sites locations (latitudes sorted) 
    # for get the acromics in crescent order
    filename = f'{acc[num]}15jan.22m'
    
    df = setting_dataframe(infile + folder, filename, 
                           component = component)
    
    df = df.loc[(df.index > tm1) & (df.index < tm2), :]

    y = df['dtrend'].values
    t = df['time'].values
    
    remove_lines(ax, acc, num)

        
    try:
        period, power = plot_LombScargle(ax, t, y, 
                             minimum_period = 0.1, 
                             maximum_period = 0.7)
        
        best_period[names[num]] = period[np.argmax(power)]
        ax.axvline(x = period[np.argmax(power)], label = 'Best period')
        ax.set(ylim = [0, 0.3], xlabel = 'Period (hours)')
    except:
        pass
    
    #Put the name of location
    ax.text(0.02, 0.7, names[num], transform = ax.transAxes)
    

avg_period = np.array(list(best_period.values())).mean()


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

#Save the plate
NameToSave = f'{ylabel}{tm1.strftime("%d%m%Y")}LombScargle.png'
#save_plot(NameToSave, dpi = 100)
plt.show()  
    

