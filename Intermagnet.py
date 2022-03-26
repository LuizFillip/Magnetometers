# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 18:49:35 2022

@author: LuizF
"""

import os.path
import sys



def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]





def get_attrs(infile, save = False):
    '''
    Get some atrributes in DataFrame format (pandas)
    from data INTERMAGNET data files from the Kyoto GIN. 
    See the website: and acknowledgment templates can be found
    at www.intermagnet.org.
    
    Parameters
    ----------
        Path: String
            Where yours files is it 
    Returns
    -------
        Defoult Station Name, IAGA CODE, Latitude and Longitude
    '''
    
    
    infos_extracted = []
    
    _, _, files = next(os.walk(infile))
    
    for filename in files:
        
        if 'min' in filename:
            
            # Read the files like string text
            with open(infile + filename) as f:
                header = f.read()
            
            # Find all indexes thats contain '/' 
            # (with separate the informations)
            idx = find(header, '|')
            
            # Use the indexes above for get the main 
            # informations
            name = replace_char(header[idx[1]: idx[2]])
            code = replace_char(header[idx[2]: idx[3]])
            
            # Convert the latitude and longitude 
            # into numeric format (float)
            lat = float(replace_char(header[idx[3]: idx[4]]))
            lon = float(replace_char(header[idx[4]: idx[5]]))
            
            # COndition for longitude
            if lon > 180:
                lon = (-360 + lon)
     
            infos_extracted.append([name, code, lat, lon])
            
    # Join the results in the DataFrame
    df = pd.DataFrame(infos_extracted, 
                      columns = ['Station', 'Code', 'Lat', 'Lon'])
    
    if save: 
        # If want the save
        df.to_csv(infile.replace('Intermag/', 'StationsCoords.txt')) 
    else:
        return df    
    
infile = 'Database/Intermag/'

    
#get_attrs(infile)