import pandas as pd
import datetime as dt 
import numpy as np 

def embrace(infile, component = None, N = 10):
    """
    Function for to organize magnetormeters data from 
    EMBRACE (INPE).
    Here, returns dTrend array from the component desired with the 
    running average. Moreover, 
    it creates more two columns for the time: 
    One in the datetime format (for dataframe index) and other it is
    running time (float array), the last can be used in numerical 
    analysis (Lomb Scargle, least squares, wavelets and others). 
    """
    
    #read csv file 
    df = pd.read_csv(infile, 
                     header = 1, delim_whitespace = True)
    #dictionary for rename columns
    columns = {
        'YYYY': 'year',
               'MM': 'month', 'DD': 'day', 
               'HH':'hour', 'MM.1':'minute'}

    df.rename(columns = columns, inplace = True)

    df.index = pd.to_datetime(
        df[['day', 'month', 
            'year', 'hour', 
             'minute']],infer_datetime_format = True)
    
    df['time'] = df['hour'] + (df['minute'] / 60)
    
    df = df.drop(columns = list(columns.values()))
    
    df.index = pd.to_datetime(df.index)
    
   
    
    if component is not None:
        
        df['dtrend'] = (df[component] - 
                        df[component].rolling(window = N).mean())
        df = df.dropna()
    
    df.index = pd.to_datetime(df.index) 
    
    
    for col in df.columns:
        df.rename(
            columns = {col: col.replace(
                "(nT)", "").replace("(Deg)", "")},
            inplace = True)
    return df


def fn2dn(file, code = 'vss'):
    fmt = f'{code}%d%b.%ym'
    return dt.datetime.strptime(file, fmt)

def dn2fn(dn, code = 'slz'):
    return dn.strftime(f'{code}%d%b.%ym').lower()

def embrace_path(dn, code = 'slz'):
    root = f'magnet/data/{dn.year}/{code.upper()}'
    return f'{root}/' +  dn2fn(dn, code)

def sub_midnight(df):
    mid = df.loc[df.index.time == dt.time(3, 0), 'H'].item()
    return df['H'] - mid

def load_embrace(dn, code):
  
    return embrace(embrace_path(dn, code = code)) 
