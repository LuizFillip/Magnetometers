# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:39:33 2022

@author: LuizF
"""

import os
import shutil
from tqdm import tqdm

import gzip


def unzip(filename, infile, file_out):
    with gzip.open(infile + filename, 'rb') as f_in:
        newname = filename.replace('.gz', '.txt')
        
        with open(newname, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            try:
                shutil.copy(newname, f'{file_out}{newname}')
                
            except:
                print('The file was it copied')
                
        os.remove(newname)
        
        
infile = "C:\\Users\\LuizF\\Downloads\\data20220324182310\\"

file_out = ("C:\\Users\\LuizF\\Google Drive\\My Drive\\Python\\doctorate-master" +
               "\\MagnetometerAnalysis\\Database\\Intermag\\")

    
files = next(os.walk(infile), (None, None, []))[2]

for filename in files:
    if '.gz' in filename:
        unzip(filename, infile, file_out)
    else:
        shutil.copy(infile + filename, f'{file_out}{filename}')
        