import magnet as mg 
import pandas as pd
from scipy.signal import savgol_filter
import datetime as dt 
import core as c 

def lt_index(df):
    lon = -48.5  # exemplo
    df["LT"] = (
        df.index.hour +
        df.index.minute / 60 +
        lon / 15
    ) % 24
    return df 

def savgol_fn(
        series, 
        win_minutes = 30, 
        polyorder = 2, 
        mode = 'interp'
        ):

    dt_min = (series.index[1] - series.index[0]) * 60

    win_pts = int(round(win_minutes / dt_min))
    if win_pts % 2 == 0:
        win_pts += 1

    y = savgol_filter(
        series.values,
        window_length = win_pts,
        polyorder = polyorder,
        mode=mode
        )
    return pd.Series(y, index=series.index, name=series.name)


def get_mean_std_filt(ds):
    df = pd.DataFrame(
        {"avg": ds.mean(axis = 1, skipna = True)}
        )
    df["std"] = ds.std(axis=1, ddof=1, skipna=True)
    
    df = df.interpolate(limit_direction="both")
    
    df['h'] = savgol_fn(df['avg'])
    
    return df 





def quiet_days(ref, code, vl = 'quiet5'):
    
    days = c.get_days_kyoto(
        ref.year,  
        ref.month, 
        vl = vl
        )

    out = []
    for dn in days:
        try:
            df = mg.load_intermag(dn, code)
        except:
            df = mg.load_embrace(dn, code)
            
        df.index = (
            df.index.hour + (df.index.minute / 60) 
        )
        out.append(df['H'].to_frame(dn))
        
    return pd.concat(out, axis = 1).sort_index()

def delta_quiet_time(ref, code = 'slz', vl = 'quiet5'):
     '''
    
     Curva de período calmo

     '''
 
     df = get_mean_std_filt( quiet_days(ref, code, vl))

     if isinstance(df.index[0], float):
         mid = df.loc[df.index == 3, 'h'].item()
     else:
         mid = df.loc[df.index.time == dt.time(3, 0), 'h'].item()
         
     df['delta_h'] = df['h'] - mid
    
     return df

def time_reindex(df, base):
    td = pd.to_timedelta(df.index, unit="h")
   
    td_rounded = td.round("1min")

    df.index = base + td_rounded
    return df 

def repeat_quiet_time(code, d_distu, d_quiet):
    out = []

    for day in d_distu:
    
        base = dt.datetime(2015, 12, day)
        
        data = delta_quiet_time(d_quiet, code= code)
        
        out.append(time_reindex(data, base))
        
    return pd.concat(out)

def  main():
    dn = dt.datetime(2025, 1, 2)
    
    code = 'ttb'
    code = 'eus'
    ref = dt.datetime(2025, 1, 1)
    delta_quiet_time(ref, code = code, vl = 'quiet5')