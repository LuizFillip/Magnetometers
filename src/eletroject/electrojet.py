import magnet as mg 
import pandas as pd 
import datetime as dt 
 

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
    
    df["dH"] = df["H"] - df["H_03"]
    return df[['H', "H_03", 'dH']]

def storm_time(days_dist, code = 'slz', 
               correct = True):
    
    out = []
    for day in days_dist:
        dn = dt.datetime(2015, 12, day)
        fn = mg.mag_path(dn, code = code)
        out.append( delta_midnight(
            mg.embrace(fn))['H_norm'])
    
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


 

# def electrojet(c1 = 'slz', c2 = 'eus'):
#     d_quiet = [3, 4, 30, 18, 28]
#     d_distu = [19, 20, 21, 22]
    
#     slz =  storm_time(d_distu, code = c1)
#     vss =  storm_time(d_distu, code = c2 )
    
#     q_slz = repeat_quiet_time(c1, d_distu, d_quiet)
#     q_vss = repeat_quiet_time(c2, d_distu, d_quiet)
    
#     df = pd.DataFrame()
    
#     df['storm'] = slz[c1] - vss[c2]
#     df['quiet'] = q_slz - q_vss 
    
#     return df.interpolate(method = 'cubic', order = 3)


 
dn = dt.datetime(2025, 1, 1)

def EEJ(dn):
    off_eq = delta_midnight(mg.load_embrace(dn, 'eus'))
    
    in_eq = delta_midnight(mg.load_intermag(dn, 'ttb'))
    
    return (in_eq['dH']  - off_eq['dH']).to_frame()

EEJ(dn)
 