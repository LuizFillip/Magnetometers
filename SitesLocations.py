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

def plot_MagneticField(ax, date, 
                       start_lon, end_lon, step_lon, 
                       start_lat, end_lat, step_lat):
    '''
    # Get modeling values from IGRF-12 (Library)
    '''
    df = table_igrf(start_lon, end_lon, step_lon, 
                   start_lat, end_lat, step_lat, 
                   date = date, 
                   coord = 'I')
    
    CS = ax.contour(df.columns, df.index, df.values, 0, cmap = 'Dark2')
    
    ax.clabel(CS, CS.levels, inline=True, fontsize = 10)

def features_of_map(fig, ax, 
                    start_lon, end_lon, step_lon, 
                    start_lat, end_lat, step_lat):
    
    '''
    Routine for plot cartoy map with all specifications
    only declaring the beginnig and ending of latitudes
    and longitudes (and yours steps). 
    
    '''

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
    
    ax.set_extent([start_lon, end_lon, start_lat, end_lat], 
              crs=ccrs.PlateCarree())

    ax.set_xticks(np.arange(start_lon, end_lon + step_lat, step_lon), 
                  crs=ccrs.PlateCarree()) 
    
    ax.set_yticks(np.arange(start_lat, end_lat + step_lat, step_lat), 
                  crs=ccrs.PlateCarree())


date = datetime.datetime(2022, 1, 15)    
    
    

fig = plt.figure(figsize = (15, 12))
ax = plt.axes(projection = ccrs.PlateCarree())


start_lat, end_lat = -90, 90 #-60, 10
start_lon, end_lon = -90, 60 #-80, -30
step_lat, step_lon = 15, 15


features_of_map(fig, ax, start_lon, end_lon, step_lon, 
                    start_lat, end_lat, step_lat)    

fontsize = 13
#names, acc, latitudes, longitudes = sites_infos(remove = None)


coords = pd.read_csv('MagnetometerAnalysis/Database/StationsCoords.txt', delimiter=',')

sts = ['Pilar', 'Tatuoca','Guimar - Tenerife', 
       'Eskdalemuir', 'Lerwick', 'Hartland', 'Hornsund']

coords = coords.loc[coords['Station'].isin(sts)].sort_values(by=['Lat'])


latitudes = pd.to_numeric(coords['Lat'].values)
longitudes = pd.to_numeric(coords['Lon'].values) 

names = coords['Station'].values

for lat, lon, name in zip(latitudes, longitudes, 
                          names):
    
    
    
    ax.plot(lon, lat, 'o', color = 'red', 
            marker = '^', markersize = 10)
    
    offset = 1
    ax.text(lon, lat + offset, name, fontsize = fontsize)
        

ax.plot([longitudes[0], longitudes[-1]], 
        [latitudes[0], latitudes[-1]], 
        color = 'k', lw = 2)

# Plot magnetic equator



def Plot_Dip(ax, 
             infile = 'GOLD/Level1C/mag_inclination_2021.txt'):
    
    df = pd.read_csv(infile, delim_whitespace = True)

    df = pd.pivot_table(df, columns = 'lon', index = 'lat', values = 'B')
    
    ax.contour(df.columns.values, df.index.values, 
               df.values, 1, linewidths = 2, color = 'k',
                   transform = ccrs.PlateCarree())
    
   

Plot_Dip(ax)

fig.suptitle((f'Intermagnet Magnetometers locations - {date.strftime("%Y/%m/%d")}'), 
             y = 0.9)


plt.rcParams.update({'font.size': fontsize})   

NameToSave = 'SitesLocationsMagnetometers.png'

save_plot(NameToSave, dpi = 100)
plt.show()
   

