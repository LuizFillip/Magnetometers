# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 21:23:21 2022

@author: LuizF
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as dates
import datetime

import os.path
import sys



class intermagnet:
    
    '''
    Get some atrributes in DataFrame format (pandas)
    from data INTERMAGNET data files from the Kyoto GIN. 
    See the website: and acknowledgment templates can be found
    at www.intermagnet.org.
    
    Parameters
    ----------
        Infile: String
           Path of direcotry where the files is it 
    Methods
    -------
        dataframe: Pandas Datraframe (datetime index and components only)
    '''
    
    def __init__(self, filename, infile):
        
        self.filename = filename
        self.infile = infile
       
        with open(self.infile + self.filename) as f:
            self.all_data = [line.strip() for line in f.readlines()]
  
        self.count = 0
        for num in range(len(self.all_data)):
            if ('DATE' or 'TIME') in self.all_data[num]:
                break
            else:
                self.count += 1
                
    def replace_char(self, text):
        
        """
        Replace, with an loop, string from a text
        """
        self.text = text
    
        for ch in ['|', 'Station Name', 'Station', 
                   'IAGA CODE', 'IAGA Code', 
                   'Geodetic Latitude', 
                   'Geodetic Longitude',
                   'Reported']:
            
            if ch in self.text:
                self.text = self.text.replace(ch,'').strip()
                
        return self.text
    
    def find(self, s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]
            
    @property        
    def report(self):
        return self.replace_char(self.all_data[7])
    
    @property        
    def code(self):
        "Acronym for the station name"
        return self.filename[:3]
    
    @property        
    def date(self):
        self.year = int(self.filename[3:7])
        self.month = int(self.filename[7:9])
        self.day = int(self.filename[9:11])
        return datetime.datetime(self.year, self.month, self.day)

    @property        
    def name(self):
        return self.replace_char(self.all_data[2])
    
    @property 
    def header(self):
        return self.count
    
    @property 
    def latitude(self):
        return float(self.replace_char(self.all_data[4]))
    
    @property 
    def longitude(self):
        self.lon = float(self.replace_char(self.all_data[5]))
        
        if self.lon > 180:
               self.lon = (-360 + self.lon)
               
        return self.lon
    
    @property
    def dataframe(self):
        
        # Read csv data files
        self.df = pd.read_csv(self.infile + self.filename, 
                         delim_whitespace = True, header = self.header)
        
        # Setting index in datetime format
        self.df.index = pd.to_datetime(self.df['DATE'] + ' ' + self.df['TIME'], 
                                  infer_datetime_format = True)
        
        self.df = self.df.drop(columns = ['DATE', 'TIME', 'DOY', '|'])
        
        # Get code file (acronym for the station name)
        code = self.code.upper()
            
        
        if self.report == 'XYZF':
            
            columns = {f'{code}X': "X", f'{code}Y': "Y", 
                       f'{code}Z': "Z", f'{code}F': "F"}
            self.df.rename(columns = columns, inplace = True)
            
            # Compute the horizontal component (Kirchoff)
            self.df['H'] = np.sqrt(self.df['X']**2 + self.df['X']**2)
            
        else:
            columns = {f"{code}H": "H", f"{code}D": "D", 
                       f"{code}Z": "Z", f"{code}F": "F"}
            
            self.df.rename(columns = columns, inplace = True)
            
            self.df['Y'] = self.df['H'] * np.sin(np.deg2rad(self.df['D']))
            
            self.df['X'] = self.df['H'] * np.cos(np.deg2rad(self.df['D']))
            
            
            self.df.index.name = self.name
        return self. df
            
def dtrend(df, component = 'H', limit = 200):
    
    "Compute dtrend (Remove the runnig average with 10 minutes)"
    
    df['dtrend'] = (df[component] - df[component].rolling(window = 10).mean())
    df['time'] = df.index.hour + (df.index.minute / 60)
    
    if limit:
        df.dtrend = df.dtrend.where(df.dtrend.between(-limit, limit))
    
    df = df.dropna()    
    return df

def get_filenames_from_codes(infile, sts = ['Pilar', 'Tatuoca',
                                            'Guimar - Tenerife', 'San Fernando',
                                            'Eskdalemuir', 'Lerwick', 
                                            'Hartland', 'Hornsund']):
    
    '''
    Find files by their code or station name (parameter: sts)
    After cross related with the directory for to get the filenames
    '''
    
    df = pd.read_csv('Database/StationsCoords.txt', 
                     delimiter=',')
    
    find_sts = df.loc[df['Station'].isin(sts)].sort_values(by=['Lat'])
    
    result = []
    
    _, _, files = next(os.walk(infile))
   
    
    for code in find_sts['Code'].values:
        for filename in files:   
            if code.lower() == filename[:3]:
                result.append(filename)
    
    return result


def main():
    files = get_filenames_from_codes('Database/Intermag/')
    
    filename = files[0]
    
    instance_ = intermagnet(filename, 'Database/Intermag/')
    df = dtrend(instance_.dataframe, component = 'X')
    print(df)
