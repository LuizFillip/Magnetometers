# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 15:21:57 2022

@author: LuizF
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
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


sites = np.array([['Rio Grande', 'rga', -53.78, -67.70],
                ['São Martinho da Serra', 'sms', -29.53,-53.85], 
                ['Tucumán', 'tcm', -26.56, -64.88], 
                ['São José Dos Campos', 'sjc', -23.19, -45.89], 
                ['Vassouras', 'vss', -22.41, -43.66],
                ['Jataí', 'jat', -17.88, -51.72], 
                ['Cuiabá', 'cba', -15.60, -56.10], 
                ['Araguatins', 'ara', -5.65, -48.12], 
                ['Eusébio', 'eus',  -3.89, -38.45], 
                ['São Luis', 'slz', -2.53, -44.30]])


#get modeling values
date = datetime.datetime(2022, 1, 15)
df = table_igrf(start_lon, end_lon, step_lon, 
               start_lat, end_lat, step_lat, 
               date = date, 
               coord = 'H')

CS = ax.contour(df.columns, df.index, df.values, 15, cmap = 'jet')

ax.clabel(CS, CS.levels, inline=True, fontsize=10)

fontsize = 12

for lat, lon, name in zip(pd.to_numeric(sites[:, 2]), 
                          pd.to_numeric(sites[:, 3]), 
                          sites[:, 0]):
    
    ax.plot(lon, lat, 'o', color = 'red', 
            marker = '^', markersize = 10)
    
    if name == 'São José Dos Campos':    
        ax.text(lon - 1.5, lat - 1.8, name, fontsize = fontsize)
    else:
        offset = 1
        ax.text(lon, lat + offset, name, fontsize = fontsize)
        
        
fig.suptitle(f'Sites locations of EMBRACE Magnetometers\n and Horizontal componente (IGRF) - {date.date()}', 
             y = 0.93)

plt.rcParams.update({'font.size': fontsize})   

NameToSave = 'SitesLocationsMagnetometers.png'
path_to_save = infile = 'G:\\My Drive\\Python\\doctorate-master\\'\
        'AtmospherePhysics\\Database\\Figures\\'

plt.savefig(path_to_save + NameToSave, dpi = 1000, bbox_inches="tight")

plt.show()
   

