# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 15:21:57 2022

@author: LuizF
"""

import os.path
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from Intermagnet import *

import cartopy.feature as cf
import cartopy.crs as ccrs
import datetime
import time
import pyIGRF

def ComputeIGRF(start_lon, end_lon, step_lon, 
               start_lat, end_lat, step_lat,
               date = datetime.datetime(2022, 1, 15), 
               coord = 'H'):
  
    """
    Running IGRF-12 ()
    
    """
    
    RT = 6370 #in km
    
    longitudes = np.arange(start_lon, end_lon + step_lon, step_lon)
    latitudes  = np.arange(start_lat, end_lat + step_lat, step_lat)
    
    def toYearFraction(date):
        
        "Return years in fraction (like julian date) "
    
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
                                                    lon, 0 * RT, date_fraction)
            data.append([lon, lat, vars()[coord]])
            
    df = pd.DataFrame(data, columns = ['Lon', 'Lat', coord])
    
    return pd.pivot_table(df, values = coord, index=['Lat'], columns=['Lon'])

def plot_MagneticField(ax, date, 
                       start_lon, end_lon, step_lon, 
                       start_lat, end_lat, step_lat):
    '''
    Get modeling values from IGRF-12 (Library). 
    The table with the data it is compute in 
    separated function ()
    '''
    df = ComputeIGRF(start_lon, end_lon, step_lon, 
                   start_lat, end_lat, step_lat, 
                   date = date, 
                   coord = 'I')
    
    CS = ax.contour(df.columns, df.index, df.values, 0, cmap = 'Dark2')
    
    ax.clabel(CS, CS.levels, inline = True, fontsize = 10)

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




def Plot(fig, ax, files, infile, dip = True, 
         fontsize = 13, save  = False):
    
    longitudes = []
    latitudes = []
    for filename in files:
        
        instance_ = intermagnet(filename, infile)
        
        lat = instance_.latitude
        lon = instance_.longitude
        name = instance_.name
        
        longitudes.append(lon)
        latitudes.append(lat)
        # Plot locations sites
        ax.plot(lon, lat, 'o', color = 'red', 
                marker = '^', markersize = 10)
        
        offset = 1
        ax.text(lon, lat + offset, name, fontsize = fontsize)
            
    # Continuous line from de lower to upper station (by latitude)
    ax.plot([longitudes[0], longitudes[-1]], 
            [latitudes[0], latitudes[-1]], 
            color = 'k', lw = 2)
    
    if dip:
        # Plot magnetic equator
        
        abs_path = 'C:/Users/LuizF/Google Drive/My Drive/Python/doctorate-master/GOLD/Level1C/mag_inclination_2021.txt'
        
        df = pd.read_csv(abs_path, 
                         delim_whitespace = True)
    
        df = pd.pivot_table(df, columns = 'lon', index = 'lat', values = 'B')
        
        ax.contour(df.columns.values, df.index.values, 
                   df.values, 1, linewidths = 2, color = 'k',
                       transform = ccrs.PlateCarree())
        
        ax.text(0, 5, 'Magnetic Equator', fontsize = fontsize)
    
   
    def date(format_ = "%d/%m/%Y"):
        return instance_.date.strftime(format_)

    fig.suptitle((f'INTERMAGNET Magnetometers locations - {date()}'), 
             y = 0.9, fontsize = fontsize)
    
    plt.rcParams.update({'font.size': fontsize})
    
    if save:
        
       NameToSave = 'SitesLocationsMagnetometers.png'
       path_to_save = 'Figures/INTERMAGNET/'
    
       plt.savefig(path_to_save + NameToSave, 
                    dpi = 100, bbox_inches="tight")
        
  
    plt.show()
   
### Plot
fig = plt.figure(figsize = (15, 12))
ax = plt.axes(projection = ccrs.PlateCarree())


start_lat, end_lat = -60, 90 #-60, 10
start_lon, end_lon = -75, 30 #-80, -30
step_lat, step_lon = 15, 15


features_of_map(fig, ax, start_lon, end_lon, step_lon, 
                    start_lat, end_lat, step_lat)    


infile = 'Database/Intermag/'

files = get_filenames_from_codes(infile)


Plot(fig, ax, files, infile, dip = True, 
         fontsize = 13, save = True)
