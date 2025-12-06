import magnet as mg 
import pandas as pd
from scipy.signal import savgol_filter
import datetime as dt 

root = 'magnet/data/2015'
 

def savgol_fn(
        series, 
        win_minutes=30, polyorder=2, mode='interp'):

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


def filter_and_avg(
    quiet: pd.DataFrame,
    std: bool = False,        # ex.: savgol_minutes
    cols=None,                 # lista de colunas (opcional)
    prefill: str | None = "interp",  
    **savgol_kwargs            # kwargs extras para o seu filtro
) -> pd.DataFrame:

  
    df = quiet.copy()
    if cols is not None:
        df = df[cols]
    else:
        df = df.select_dtypes(include="number")

    if df.empty:
        return pd.DataFrame(index=quiet.index)

    # tratamento de NaNs sem perder o índice
    if prefill == "interp":
        df = df.interpolate(limit_direction="both")
    elif prefill == "ffill":
        df = df.ffill()
    elif prefill == "bfill":
        df = df.bfill()
 
    filtered = df.apply(lambda s: savgol_fn(s, **savgol_kwargs))

    # monta saída
    out = pd.DataFrame(
        {"h": filtered.mean(axis=1, skipna=True)})
    if std:
        out["std"] = filtered.std(
            axis=1, ddof=1, skipna=True)

    return out

def jump_correction(s, offset = 20):
    dates = s.index.normalize()
    
    g = s.groupby(dates)
    first = g.first()   # primeiro valor de cada dia
    last  = g.last()    # último valor de cada dia
    
    # salto entre dias: primeiro de hoje - último de ontem
    jump = first - last.shift(1)
    
    jump.iloc[0] = 0
    
    jump = jump.where(jump.abs() > offset, 0)
    
    corr_per_day = jump.cumsum()         # índice = datas
    
    corr = corr_per_day.reindex(dates).to_numpy()
    
    return s - corr

def delta_midnight(df):
    h3 = df.between_time("03:00", "03:00")["H"]
    
    h3.index = h3.index.date
    
    df["H_03"] = df.index.date
    df["H_03"] = df["H_03"].map(h3)
    
    df["H_norm"] = df["H"] - df["H_03"]
    return df 

def storm_time(days_dist, code = 'slz', 
               correct = True):
    
    out = []
    for day in days_dist:
        dn = dt.datetime(2015, 12, day)
        fn = mg.mag_path(dn, code = code)
        out.append( delta_midnight(mg.embrace(fn))['H_norm'])
    
    ds = pd.concat(out)
    if correct:
        ds = jump_correction(ds)
    return ds.to_frame(code)


def quiet_time(days, code = 'slz'):
    
    out = []
    for day in days:
        dn = dt.datetime(2015, 12, day)
        fn = mg.mag_path(dn, code = code)
        df = mg.embrace(fn).set_index('time')
    
        out.append(df['H'].to_frame(day))
        
    return pd.concat(out, axis = 1)


def delta_quiet_time(d_quiet, code = 'slz'):
    
    qt = filter_and_avg(quiet_time(d_quiet, code= code))
    
    mid = qt.loc[qt.index == 3, 'h'].item()
    
    qt['h'] = qt['h'] - mid
    
    return qt

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
    

def electrojet(c1 = 'slz', c2 = 'eus'):
    d_quiet = [3, 4, 30, 18, 28]
    d_distu = [19, 20, 21, 22]
    
    slz =  storm_time(d_distu, code = c1)
    vss =  storm_time(d_distu, code = c2 )
    
    q_slz = repeat_quiet_time(c1, d_distu, d_quiet)
    q_vss = repeat_quiet_time(c2, d_distu, d_quiet)
    
    df = pd.DataFrame()
    
    df['storm'] = slz[c1] - vss[c2]
    df['quiet'] = q_slz - q_vss 
    
    return df.interpolate(method = 'cubic', order = 3)



