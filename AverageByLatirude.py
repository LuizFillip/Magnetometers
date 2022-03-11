# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 23:14:31 2022

@author: LuizF
"""

import matplotlib.pyplot as plt
import numpy as np
import datetime
import os.path
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from MagnetometersAnalysis import *

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

infile = 'G:\\My Drive\\Python\\doctorate-master\\'\
        'AtmospherePhysics\\Database\\'
        
folder = 'Magnetometer15012022'

fmtdate = folder.replace('Magnetometer', '')

day = int(fmtdate[:2])
mon = int(fmtdate[2:4])
yer = int(fmtdate[4:])


acc = sites[:, 1]
names = sites[:, 0]

data = {'Horizontal (H)' : [], 
        'Vertical (Z)': []}

for num in range(len(acc)):
    
    # Use the sites locations (latitudes sorted) 
    # for get the acromics in crescent order
    filename = f'\\{acc[num]}{day}jan.22m'
           
    # Read the files
    df = setting_dataframe(infile + folder, filename)
    

    data['Horizontal (H)'].append(df['H(nT)'].mean())
    data['Vertical (Z)'].append(df['Z(nT)'].mean())

  
rs = pd.DataFrame(data, index = names)

fig, ax = plt.subplots(figsize = (9, 4))

rs.plot(kind='barh', ax = ax, color = ('k', '#1f77b4'))

ax.set(xlabel = 'Dialy average of components (nT)', 
       title = f'EMBRACE magnetometers \n magnitudes comparation - {yer}-{mon}-{day}')

NameToSave = f'{day}{mon}{yer}MagntudeComparation.png'
path_to_save = infile + 'Figures\\'

ax.legend(loc = 'upper left', 
          ncol = 1, fontsize = 14)

plt.savefig(path_to_save + NameToSave, dpi = 1000)

plt.show()

