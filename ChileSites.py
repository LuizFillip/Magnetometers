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

#550001,"Guardiamarina Zanartu, Pto Williams Ad.",SCGZ,-54.93167,-67.61556
#270001,Mataveri Isla de Pascua Ap.,SCIP,-27.15889,-109.4325
#220002,"El Loa, Calama Ad.",SCCF,-22.49806,-68.8925

embrace = "G:/Meu Drive/Python/doctorate-master/MagnetometerAnalysis/Database/Magnetometer15012022/"
interma = "G:/Meu Drive/Python/doctorate-master/MagnetometerAnalysis/Database/Intermag/"

latitudes = pd.to_numeric(x[:, 2])
longitudes = pd.to_numeric(x[:, 3])
names = x[:, 0]



        

nrows = 3
ncols = 2

fig, axs = plt.subplots(figsize = (12, 10), 
                      nrows = nrows, 
                      ncols = ncols)

plt.subplots_adjust(hspace = 0, wspace = 0)

remove_lines(axs, nrows, ncols)
fontsize = 15

axs[0, 0].set(title = 'Magnetometers Stations')
axs[0, 1].set(title = 'Pressure Stations')


for num, ax in enumerate(axs.flat):
    
    filename = files[num]
    
    if '15jan.22m' in filename:
        infile = embrace
       
        df = em.setting_dataframe(infile, filename)
    
        ax.plot(df['dtrend'], color = 'k', lw = 1)
        name = x[(x[:, 1] == filename[:3])][0][0]
                
        ax.set(ylim = [-10, 10])
        
    elif "min" in filename:
        infile = interma
        #ax1 = ax.twinx()
        instance_ = it.intermagnet(filename, infile)
        df = it.dtrend(instance_.dataframe)
        ax.plot(df['dtrend'], color = 'k', lw = 1)
        name = x[(x[:, 1] == filename[:3])][0][0]
        ax.set(ylim = [-10, 10])
    else:
       
        ax1 = ax.twinx()
        df = ChilePressure(filename)
    
        ax1.plot(df['dtrend'], color = 'k', lw = 1)
        name = x[(x[:, 1] == filename)][0][0]
        
        if num == 1:    
            ax1.spines['bottom'].set_visible(False)  
            ax1.spines['left'].set_visible(False)
        elif num == (nrows*ncols - 1):    
            ax1.spines['top'].set_visible(False)
            ax1.spines['left'].set_visible(False)
        elif num // 2 != 0:
            ax1.spines['top'].set_visible(False)
            ax1.spines['bottom'].set_visible(False)
            ax1.spines['left'].set_visible(False)
            
        
        ax1.set(ylim = [-1, 0.9])
    
    ax.text(0.03, 0.8, name, transform = ax.transAxes)

    ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
    ax.xaxis.set_major_locator(dates.HourLocator(interval = 2))
    
    
fig.text(0.06, 0.5, 'Horizontal component (nT)', va='center', 
             rotation='vertical', fontsize = fontsize)   

fig.text(0.97, 0.5, 'Pressure variation (mbar)', va='center', 
             rotation='vertical', fontsize = fontsize)   

fig.text(0.45, 0.08, 'Universal time (UT)', va='center', 
             rotation='horizontal', fontsize = fontsize) 

fig.suptitle(f'dTrend Analysis - 15/01/2022', 
             y = 0.94, fontsize = 20)


path_to_save = 'PressureAnalysis/Figures/'
 
plt.savefig(path_to_save + 'MagnetometersPressureDtrendChile.png', 
         dpi = 100, bbox_inches="tight")

