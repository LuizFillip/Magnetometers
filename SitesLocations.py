# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 15:21:57 2022

@author: LuizF
"""

import os.path
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from MagnetometersAnalysis import *


infile = 'G:\\My Drive\\Python\\doctorate-master\\MagnetometerAnalysis\\Database\\'

import cartopy.feature as cf
import cartopy.crs as ccrs
import datetime
import time
import pyIGRF

def table_igrf(start_lon, end_lon, step_lon, 
               start_lat, end_lat, step_lat,
               date = datetime.datetime(2022, 1, 15), 
               coord = 'H'):
  
    
    
    RT = 6370 #in km
    
    longitudes = np.arange(start_lon, end_lon + step_lon, step_lon)
    latitudes  = np.arange(start_lat, end_lat + step_lat, step_lat)
    
    def toYearFraction(date):
    
       # returns seconds since epoch
        def sinceEpoch(date): # returns seconds since epoch
            return time.mktime(date.timetuple())
        s = sinceEpoch
        
        year = date.year
        startOfThisYear = datetime.datetime(year = year, 
                                            month = 1, day = 1)
        startOfNextYear = datetime.datetime(year = year + 1, 
                                            month = 1, 
                                            day = 1)
        
        yearElapsed = s(date) - s(startOfThisYear)
        yearDuration = s(startOfNextYear) - s(startOfThisYear)
        fraction = yearElapsed/yearDuration
        
        return date.year + fraction

    date_fraction = toYearFraction(date)

    data = []
    
    for lon in longitudes:
        for lat in latitudes:
            D, I, H, X, Y, Z, F = pyIGRF.igrf_value(lat, 
                                                    lon, 0, date_fraction)
            data.append([lon, lat, vars()[coord]])
            
    df = pd.DataFrame(data, columns = ['Lon', 'Lat', coord])
    
    return pd.pivot_table(df, values = coord, index=['Lat'], columns=['Lon'])



def features_of_map(ax):

    ax.set_global()
    ax.gridlines(color = 'grey', linestyle = '--', crs=ccrs.PlateCarree())

    states_provinces = cf.NaturalEarthFeature(
                        category='cultural',
                        name='admin_1_states_provinces_lines',
                        scale='50m',
                        facecolor='none')


    ax.add_feature(states_provinces, edgecolor='black')
    ax.add_feature(cf.COASTLINE, edgecolor='black', lw = 2) 
    ax.add_feature(cf.BORDERS, linestyle='-', edgecolor='black')
    
    ax.set(ylabel = 'Latitude (°)', xlabel = 'Longitude (°)')
    

fig = plt.figure(figsize=(14, 10))
ax = plt.axes(projection=ccrs.PlateCarree())


features_of_map(ax)    
start_lat, end_lat = -60, 10
start_lon, end_lon = -80, -30
step_lat, step_lon = 5, 5

ax.set_extent([start_lon, end_lon, start_lat, end_lat], 
              crs=ccrs.PlateCarree())

ax.set_xticks(np.arange(start_lon, end_lon + step_lat, step_lon), 
              crs=ccrs.PlateCarree()) 

ax.set_yticks(np.arange(start_lat, end_lat + step_lat, step_lat), 
              crs=ccrs.PlateCarree())


# Get modeling values from IGRF-12 (Library)
date = datetime.datetime(2022, 1, 15)

df = table_igrf(start_lon, end_lon, step_lon, 
               start_lat, end_lat, step_lat, 
               date = date, 
               coord = 'H')

CS = ax.contour(df.columns, df.index, df.values, 15, cmap = 'jet')

ax.clabel(CS, CS.levels, inline=True, fontsize = 10)

fontsize = 13
names, acc, latitudes, longitudes = sites_infos(remove = None)


for lat, lon, name in zip(latitudes, longitudes, 
                          names):
    
    ax.plot(lon, lat, 'o', color = 'red', 
            marker = '^', markersize = 10)
    
    if name == 'São José Dos Campos':    
        ax.text(lon - 2.2, lat - 1.9, name, fontsize = fontsize)
    else:
        offset = 1
        ax.text(lon, lat + offset, name, fontsize = fontsize)
        

    
fig.suptitle(('Sites locations of EMBRACE Magnetometers\n'+
              f'and Horizontal componente (IGRF) - {date.strftime("%Y/%m/%d")}'), 
             y = 0.94)

plt.rcParams.update({'font.size': fontsize})   

NameToSave = 'SitesLocationsMagnetometers.png'

save_plot(NameToSave, dpi = 100)
plt.show()
   

