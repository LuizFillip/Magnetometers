import datetime
import time
import pyIGRF
import numpy as np
import pandas as pd

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