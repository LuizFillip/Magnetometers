import pandas as pd
import numpy as np
import datetime
import datetime as dt 
import os 

class intermagnet:
    
    '''
    Get some atrributes in DataFrame format (pandas)
    from data INTERMAGNET data files from the Kyoto GIN. 
    See the website: and acknowledgment templates can be found
    at www.intermagnet.org.
    
    Parameters
    ----------
        Infile: String
           Path of direcotry where the files is it 
    Methods
    -------
        dataframe: Pandas Datraframe 
        (datetime index and components only)
    '''
    
    def __init__(self, filename, infile):
        
        self.filename = filename
        self.infile = infile
       
        with open(self.infile + self.filename) as f:
            self.all_data = [line.strip() for line in f.readlines()]
  
        self.count = 0
        for num in range(len(self.all_data)):
            if ('DATE' or 'TIME') in self.all_data[num]:
                break
            else:
                self.count += 1
                
    def replace_char(self, text):
        
        """
        Replace, with an loop, string from a text
        """
        self.text = text
    
        for ch in ['|', 'Station Name', 'Station', 
                   'IAGA CODE', 'IAGA Code', 
                   'Geodetic Latitude', 
                   'Geodetic Longitude',
                   'Reported']:
            
            if ch in self.text:
                self.text = self.text.replace(ch,'').strip()
                
        return self.text
    
    def find(self, s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]
            
    @property        
    def report(self):
        return self.replace_char(self.all_data[7])
    
    @property        
    def code(self):
        "Acronym for the station name"
        return self.filename[:3]
    
    @property        
    def date(self):
        self.year = int(self.filename[3:7])
        self.month = int(self.filename[7:9])
        self.day = int(self.filename[9:11])
        return datetime.datetime(self.year, self.month, self.day)

    @property        
    def name(self):
        return self.replace_char(self.all_data[2])
    
    @property 
    def header(self):
        return self.count
    
    @property 
    def latitude(self):
        return float(self.replace_char(self.all_data[4]))
    
    @property 
    def longitude(self):
        self.lon = float(self.replace_char(self.all_data[5]))
        
        if self.lon > 180:
               self.lon = (-360 + self.lon)
               
        return self.lon
    
    @property
    def dataframe(self):
        
        # Read csv data files
        self.df = pd.read_csv(
            self.infile + self.filename, 
            delim_whitespace = True,
            header = self.header)
        
        # Setting index in datetime format
        self.df.index = pd.to_datetime(
            self.df['DATE'] + ' ' + self.df['TIME'], 
            infer_datetime_format = True)
        
        self.df = self.df.drop(
            columns = ['DATE', 'TIME', 'DOY', '|']
            )
        
        # Get code file (acronym for the station name)
        code = self.code.upper()
            
        
        if self.report == 'XYZF':
            
            columns = {f'{code}X': "X", f'{code}Y': "Y", 
                       f'{code}Z': "Z", f'{code}F': "F"}
            self.df.rename(columns = columns, inplace = True)
            
            # Compute the horizontal component (Kirchoff)
            self.df['H'] = np.sqrt(self.df['X']**2 + self.df['X']**2)
            
        else:
            columns = {f"{code}H": "H", f"{code}D": "D", 
                       f"{code}Z": "Z", f"{code}F": "F"}
            
            self.df.rename(
                columns = columns, inplace = True)
            
            self.df['Y'] = self.df['H'] * np.sin(
                np.deg2rad(self.df['D']))
            
            self.df['X'] = self.df['H'] * np.cos(
                np.deg2rad(self.df['D']))
            
            
            self.df.index.name = self.name
        return self. df
            
def dtrend(df, component = 'H', limit = 200):
    
    "Compute dtrend (Remove the runnig average with 10 minutes)"
    
    df['dtrend'] = (df[component] - df[component].rolling(window = 10).mean())
    df['time'] = df.index.hour + (df.index.minute / 60)
    
    if limit:
        df.dtrend = df.dtrend.where(df.dtrend.between(-limit, limit))
    
    df = df.dropna()    
    return df



pathin = 'magnetometers/data/2015/SJG/'

# Função para verificar se uma linha é numérica
def is_numeric_line(line):
    parts = line.strip().split()
    return all(part.lstrip('-').isdigit() for part in parts)

# Função para ler o arquivo e extrair os dados
def read_text_file(filename):
    data = []

    with open(filename, 'r') as file:
        for line in file:
            if is_numeric_line(line):
             
                numbers = list(map(int, line.strip().split()))
                data.append(numbers)
            else:
                # Se quiser armazenar o texto também:
                # print("Linha de texto encontrada:", line.strip())
                pass

    return data

def fn2dn(fn):
    strc = fn.split('.')[0].lower()
    return dt.datetime.strptime(strc, '%b%d%y')


fn = 'dec1915.sjg'


def to_frame(infile):
    l =  infile 
    dn  = fn2dn(l.split('/')[-1])

    data = read_text_file(infile)
    
    cols = ['x', 'y', 'z', 'f']
    
    df = pd.DataFrame(data).iloc[:, :4]
    
    df.columns = cols 
    
    times = pd.date_range(
        dn, 
        freq = '1min', 
        periods = len(df)
        )
    
    df.index = times 
    
    return df 
