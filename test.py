# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 21:23:21 2022

@author: LuizF
"""

import pandas as pd
import os
import datetime
import os.path
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from Intermagnet import *



def replace_char(text):
    
    for ch in ['|', 'Station Name', 'Station', 
               'IAGA CODE', 'IAGA Code', 
               'Geodetic Latitude', 
               'Geodetic Longitude',
               'Reported']:
        
        if ch in text:
            text = text.replace(ch,'').strip()
            
    return text

class intermaget:
    
    def __init__(self, filename, infile):
        
        self.filename = filename
        self.infile = infile
       
        with open(self.infile + self.filename) as f:
            all_data = [line.strip() for line in f.readlines()]
  
        count = 0
        for num in range(len(all_data)):
            if 'DATE' in all_data[num]:
                break
            else:
                count += 1
            
    @property        
    def report(self):
        return replace_char(all_data[7])
    
    @property        
    def code(self):
        return self.filename[:3]
    
    @property        
    def date(self):
        year = int(self.filename[3:7])
        month = int(self.filename[7:9])
        day = int(self.filename[9:11])
        return datetime.datetime(year, month, day)

    @property        
    def name(self):
        #Station name
        return replace_char(all_data[2])
    
    @property 
    def header(self):
        return count
    
    @property 
    def latitude(self):
        return float(replace_char(all_data[4]))
    
    @property 
    def longitude(self):
        self.lon = float(replace_char(all_data[5]))
        if self.lon > 180:
               self.lon = (-360 + self.lon)
        return self.lon

def get_coords():
    df = pd.read_csv('Database/StationsCoords.txt', 
                     delimiter=',')
    
    sts = ['Pilar', 'Tatuoca','Guimar - Tenerife', 
           'Eskdalemuir', 'Lerwick', 'Hartland', 'Hornsund']
    
    find_sts = df.loc[df['Station'].isin(sts)].sort_values(by=['Lat'])
    
    return find_sts['Code'].values
    
    

def setting_dataframe(infile, filename):
    
    x = intermaget(filename, infile)
    
    df = pd.read_csv(infile + filename, 
                     delim_whitespace = True, header = x.header)
    
    df.index = pd.to_datetime(df['DATE'] + ' ' + df['TIME'], 
                              infer_datetime_format = True)
    
    df = df.drop(columns = ['DATE', 'TIME', 'DOY', '|'])
    
    code = x.code.upper()
    
    if x.report == 'XYZF':
        
        columns = {f'{code}X': 'X', f'{code}Y': 'Y', 
                   f'{code}Z': "Z", f'{code}F': 'F'}
    else:
        columns = {f'{code}H': 'H', f'{code}D': 'D', 
                   f'{code}Z': "Z", f'{code}F': 'F'}
        
    df.rename(columns = columns, inplace = True)
    
    return df

infile = 'Database/Intermag/'

_, _, files = next(os.walk(infile))

filename = 'gui20220115vmin.min.txt'

df = setting_dataframe(infile, filename)

print(df)

