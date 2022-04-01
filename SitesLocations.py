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
from Embrace import *
import cartopy.feature as cf
import cartopy.crs as ccrs


def features_of_map(start_lon, end_lon, step_lon, 
                    start_lat, end_lat, step_lat):
    
    fig = plt.figure(figsize = (15, 12))
    ax = plt.axes(projection = ccrs.PlateCarree())

    '''
    Routine for plot cartoy map with all specifications
    only declaring the beginnig and ending of latitudes
    and longitudes (and yours steps). 
    
    '''

    ax.set_global()
    
    ax.gridlines(color = 'grey', linestyle = '--', 
                 crs=ccrs.PlateCarree())

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
    
    
    plt.rcParams.update({'font.size': 15})
    
    return fig, ax




def Plot_from_files(fig, ax, files, infile, dip = True, 
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
                marker = 's', markersize = fontsize)
        
        offset = 1
        ax.text(lon, lat + offset, name, fontsize = fontsize)
            
    # Plot Continuous line from de lower to upper station (by latitude)
    #ax.plot([longitudes[0], longitudes[-1]], 
    #        [latitudes[0], latitudes[-1]], 
    #        color = 'k', lw = 2)
    
    if dip:
        # Plot magnetic equator
        
        abs_path = "G:\My Drive\Python\doctorate-master\GOLD\mag_inclination_2021.txt"
        
        df = pd.read_csv(abs_path, 
                         delim_whitespace = True)
    
        df = pd.pivot_table(df, columns = 'lon', 
                            index = 'lat', values = 'B')
        
        ax.contour(df.columns.values, df.index.values, 
                   df.values, 1, linewidths = 2, color = 'k',
                       transform = ccrs.PlateCarree())
        
        #ax.text(0, 5, 'Magnetic Equator', fontsize = fontsize)
    
   
    def date(date = instance_.date, 
             format_ = "%d/%m/%Y"):
        return date.strftime(format_)

    #fig.suptitle((f'INTERMAGNET Magnetometers locations - {date()}'), 
    #         y = 0.9, fontsize = fontsize)
    
    
    
    if save:
        
       NameToSave = 'SitesLocationsMagnetometers.png'
       path_to_save = 'Figures/INTERMAGNET/'
    
       plt.savefig(path_to_save + NameToSave, 
                    dpi = 100, bbox_inches="tight")
        
  
    plt.show()
   
start_lat, end_lat = -60, 5 #-60, 10
start_lon, end_lon = -75, -30 #-80, -30
step_lat, step_lon = 5, 5

    
fig, ax = features_of_map(start_lon, end_lon, step_lon, 
                        start_lat, end_lat, step_lat)   

def Plot_EMBRACE(fig, ax): 
    
    names, acronym, lat, lon = sites_infos(remove = (3, 5))
    
 
    fontsize = 14
   #infile = 'MagnetometerAnalysis/Database/EmbraceLocations.txt'

    for num in range(len(names)):
        ax.plot(lon[num], lat[num], 
                color = 'red', 
                marker = '^', markersize = fontsize)
         
        offset = 1
        ax.text(lon[num], lat[num] + offset, 
                names[num], fontsize = fontsize)
        
        
Plot_EMBRACE(fig, ax)

files_intermagnet = ['pil20220115pmin.min.txt', 
                    'ttb20220115qmin.min']

Plot_from_files(fig, ax, files_intermagnet, 'Database/Intermag/', 
                dip = True, fontsize = 14, save = False)