# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 23:39:26 2022

@author: Luiz
"""

x = np.array([['Tucumán', 'tcm', -26.56, -64.88],
                ['Isla de Pascua', 'ipm', -27.171, -109.41], 
                ['Rio Grande', 'rga', -53.78, -67.70], 
                ["Guardiamarina Zanartu", "550001", -54.93,-67.61],
                ["Isla de Pascua", "270001", -27.158,-109.43], 
                ["El Loa, Calama", "220002", -22.49,-68.89]])


files = ['tcm15jan.22m', "220002", 
        'ipm20220115vmin.min.txt', "270001", 
        "rga15jan.22m", "550001"]

filename = files[1]
name = x[(x[:, 1] == filename)][0][0]

print(name)

## COmparation in brazil
files = ['sms15jan.22m', 'smar0151.txt', 
        'vss15jan.22m',  'eesc0151.txt', 
        'ara15jan.22m', 'topl0151_n.txt', 
        'eus15jan.22m', 'ceeu0151.txt']

pre_infile = 'PressureAnalysis/Database/station_data_brasil/'
mag_infile = 'MagnetometerAnalysis/Database/Magnetometer15012022/'

x = np.array([['Rio Grande', 'rga', -53.78, -67.70],
                ['São Martinho da Serra/RS', 'sms', -29.53,-53.85], 
                ['Tucumán', 'tcm', -26.56, -64.88], 
                ['São José Dos Campos', 'sjc', -23.19, -45.89], 
                ['Vassouras/RJ', 'vss', -22.41, -43.66],
                ['Jataí', 'jat', -17.88, -51.72], 
                ['Cuiabá', 'cba', -15.60, -56.10], 
                ['Araguatins/TO', 'ara', -5.65, -48.12], 
                ['Eusébio/CE', 'eus',  -3.89, -38.45], 
                ['São Luis', 'slz', -2.53, -44.30],
                ["Pilar", "pil", -31.7, -63.89],
                ["Tatuoca", "ttb", -1.205, -48.51]])


    
    if '15jan.22m' in filename:
        infile = mag_infile
        df = mg.setting_dataframe(infile, filename)
        im = Wavelet(df, ax, transform = 'power')
       
        name = x[(x[:, 1] == filename[:3])][0][0]
                

    else:
        infile = pre_infile
   
        df = pr.setting_dataframe(infile, filename)
        im = Wavelet(df, ax, transform = 'power')

        name = infos_met(filename).infos[0]
        
            
    