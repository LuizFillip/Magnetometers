import magnetometers as mg 
import matplotlib.pyplot as plt 
import pandas as pd
from scipy.signal import savgol_filter



def plot_days_and_getavg(days, code = 'slz', ax = None):
    
    root = 'magnetometers/data/2015'
    
    out = []
    for day in days:
        fn = f'{root}/{code}{day}dec.15m'
        df = mg.embrace(fn)
        df = df.set_index('time')
        
        out.append(df['H'].to_frame(day))
        
        if ax is not None:
            ax.plot(df['H'])
        
    ds = pd.concat(out, axis = 1)
    if ax is not None:
        ax.plot(ds.mean(axis = 1), lw = 4, color = 'k')
    
    return ds

def savgol_minutes(
        series, 
        win_minutes=30, polyorder=2, mode='interp'):
    # série com índice em horas (float ou datetime)
    # calcula o passo médio em minutos
    dt_min = (series.index[1] - series.index[0]) * 60

    win_pts = int(round(win_minutes / dt_min))
    if win_pts % 2 == 0:
        win_pts += 1

    y = savgol_filter(series.values,
                      window_length=win_pts,
                      polyorder=polyorder,
                      mode=mode)
    return pd.Series(y, index=series.index, name=series.name)

def filter_and_avg(quiet):
    for col in quiet.columns:
        quiet[col] = savgol_minutes(quiet[col].dropna())
        
    qt = pd.DataFrame()
    
    qt['std'] = quiet.std(axis = 1)
    qt['h'] = quiet.mean(axis = 1)
    return qt 


fig, ax = plt.subplots(
    nrows= 3, 
    sharex = True, 
    # sharey = True, 
    figsize = (12, 8)
    )

plt.subplots_adjust(hspace = 0.1)

days = [13, 16, 18, 29]
code = 'slz'
quiet = plot_days_and_getavg(days, code= code, ax = ax[0])


qt = filter_and_avg(quiet)

ax[1].fill_between(
    qt.index, 
    qt['h'] - qt['std'], 
    qt['h'] + qt['std'], 
    color = "red", 
    alpha = 0.3
    )

ax[1].plot(qt['h'], color = 'red')

ax[1].axvline(3, color = 'k', lw = 3, linestyle = '--')

mid = qt.loc[qt.index == 3, 'h'].item()

ax[2].plot(qt['h'] - mid, label = '$\delta H$ (vassouras)')

