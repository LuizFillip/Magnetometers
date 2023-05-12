import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import Embrace as em
import Intermagnet as it
from PressureAnalysis.remove_lines import *

def ChilePressure(filename):
    
    filename = filename + "_202201_PresionHumedad.csv"

    infile = "C:\\Users\\Luiz\\Downloads\\station_data_chile\\"

    df = pd.read_csv(infile + filename, delimiter = ";")

    df.index = pd.to_datetime(df.momento)
    
    df['time'] = df.index.hour + (df.index.minute / 60)
    
    df = df.loc[df.index.day == 15, ["p0", "time"]]

    df['dtrend'] = (df["p0"] - df["p0"].rolling(window = 10).mean())
    
    df = df.dropna()
    
    df.index.name = ''
    return df





files = ['tcm15jan.22m', "220002", 
        'ipm20220115vmin.min.txt', "270001", 
        "rga15jan.22m", "550001"]


x = np.array([['Tucumán', 'tcm', -26.56, -64.88],
                ['Isla de Pascua', 'ipm', -27.171, -109.41], 
                ['Rio Grande', 'rga', -53.78, -67.70], 
                ["Guardiamarina Zanartu", "550001", -54.93,-67.61],
                ["Isla de Pascua", "270001", -27.158,-109.43], 
                ["El Loa, Calama", "220002", -22.49,-68.89]])

