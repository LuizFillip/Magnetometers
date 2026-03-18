# import pandas as pd
# import numpy as np
# import datetime
# import datetime as dt 
# import os 

# class intermagnet:
    
#     '''
#     Get some atrributes in DataFrame format (pandas)
#     from data INTERMAGNET data files from the Kyoto GIN. 
#     See the website: and acknowledgment templates can be found
#     at www.intermagnet.org.
    
#     Parameters
#     ----------
#         Infile: String
#            Path of direcotry where the files is it 
#     Methods
#     -------
#         dataframe: Pandas Datraframe 
#         (datetime index and components only)
#     '''
    
#     def __init__(self, infile):
         
#         self.infile = infile
       
#         with open(self.infile + self.filename) as f:
#             self.all_data = [line.strip() for line in f.readlines()]
  
#         self.count = 0
#         for num in range(len(self.all_data)):
#             if ('DATE' or 'TIME') in self.all_data[num]:
#                 break
#             else:
#                 self.count += 1
                
#     def replace_char(self, text):
        
#         """
#         Replace, with an loop, string from a text
#         """
#         self.text = text
    
#         for ch in ['|', 'Station Name', 'Station', 
#                    'IAGA CODE', 'IAGA Code', 
#                    'Geodetic Latitude', 
#                    'Geodetic Longitude',
#                    'Reported']:
            
#             if ch in self.text:
#                 self.text = self.text.replace(ch,'').strip()
                
#         return self.text
    
#     def find(self, s, ch):
#         return [i for i, ltr in enumerate(s) if ltr == ch]
            
#     @property        
#     def report(self):
#         return self.replace_char(self.all_data[7])
    
#     @property        
#     def code(self):
#         "Acronym for the station name"
#         return self.filename[:3]
    
#     @property        
#     def date(self):
#         self.year = int(self.filename[3:7])
#         self.month = int(self.filename[7:9])
#         self.day = int(self.filename[9:11])
#         return datetime.datetime(self.year, self.month, self.day)

#     @property        
#     def name(self):
#         return self.replace_char(self.all_data[2])
    
#     @property 
#     def header(self):
#         return self.count
    
#     @property 
#     def latitude(self):
#         return float(self.replace_char(self.all_data[4]))
    
#     @property 
#     def longitude(self):
#         self.lon = float(self.replace_char(self.all_data[5]))
        
#         if self.lon > 180:
#                self.lon = (-360 + self.lon)
               
#         return self.lon
    
#     @property
#     def dataframe(self):
        
#         # Read csv data files
#         self.df = pd.read_csv(
#             self.infile + self.filename, 
#             delim_whitespace = True,
#             header = self.header)
        
#         # Setting index in datetime format
#         self.df.index = pd.to_datetime(
#             self.df['DATE'] + ' ' + self.df['TIME'], 
#             infer_datetime_format = True)
        
#         self.df = self.df.drop(
#             columns = ['DATE', 'TIME', 'DOY', '|']
#             )
        
#         # Get code file (acronym for the station name)
#         code = self.code.upper()
            
        
#         if self.report == 'XYZF':
            
#             columns = {f'{code}X': "X", f'{code}Y': "Y", 
#                        f'{code}Z': "Z", f'{code}F': "F"}
#             self.df.rename(columns = columns, inplace = True)
            
#             # Compute the horizontal component (Kirchoff)
#             self.df['H'] = np.sqrt(self.df['X']**2 + self.df['X']**2)
            
#         else:
#             columns = {f"{code}H": "H", f"{code}D": "D", 
#                        f"{code}Z": "Z", f"{code}F": "F"}
            
#             self.df.rename(
#                 columns = columns, inplace = True)
            
#             self.df['Y'] = self.df['H'] * np.sin(
#                 np.deg2rad(self.df['D']))
            
#             self.df['X'] = self.df['H'] * np.cos(
#                 np.deg2rad(self.df['D']))
            
            
#             self.df.index.name = self.name
#         return self. df
            
# def dtrend(df, component = 'H', limit = 200):
    
#     "Compute dtrend (Remove the runnig average with 10 minutes)"
    
#     df['dtrend'] = (df[component] - df[component].rolling(window = 10).mean())
#     df['time'] = df.index.hour + (df.index.minute / 60)
    
#     if limit:
#         df.dtrend = df.dtrend.where(df.dtrend.between(-limit, limit))
    
#     df = df.dropna()    
#     return df



import os
import datetime as dt
import numpy as np
import pandas as pd


class Intermagnet:
    """
    Read INTERMAGNET data files from Kyoto GIN and return metadata
    and magnetic components as a pandas DataFrame.
    """

    def __init__(self, infile):
        self.filepath = infile
        self.infile = os.path.dirname(infile)
        self.filename = os.path.basename(infile)

        with open(self.filepath, "r", encoding="utf-8", errors="ignore") as f:
            self.all_data = [line.strip() for line in f.readlines()]

        self.count = 0
        for line in self.all_data:
            if ("DATE" in line) and ("TIME" in line):
                break
            self.count += 1

    def replace_char(self, text):
        """
        Remove known header labels from metadata lines.
        """
        cleaned = text
        for ch in [
            "|",
            "Station Name",
            "Station",
            "IAGA CODE",
            "IAGA Code",
            "Geodetic Latitude",
            "Geodetic Longitude",
            "Reported",
        ]:
            cleaned = cleaned.replace(ch, "").strip()
        return cleaned

    def find(self, s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    @property
    def report(self):
        return self.replace_char(self.all_data[7])

    @property
    def code(self):
        return self.filename[:3].upper()

    @property
    def date(self):
        year = int(self.filename[3:7])
        month = int(self.filename[7:9])
        day = int(self.filename[9:11])
        return dt.datetime(year, month, day)

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
        lon = float(self.replace_char(self.all_data[5]))
        if lon > 180:
            lon = lon - 360
        return lon

    @property
    def dataframe(self):
        df = pd.read_csv(
            self.filepath,
            sep=r"\s+",
            header=self.header,
            engine="python"
        )

        # datetime index
        df.index = pd.to_datetime(df["DATE"] + " " + df["TIME"])
        df.index.name = self.name

        # remove auxiliary columns if present
        drop_cols = [c for c in ["DATE", "TIME", "DOY", "|"] if c in df.columns]
        df = df.drop(columns=drop_cols)

        code = self.code

        if self.report == "XYZF":
            columns = {
                f"{code}X": "X",
                f"{code}Y": "Y",
                f"{code}Z": "Z",
                f"{code}F": "F",
            }
            df = df.rename(columns=columns)

            # horizontal component
            if {"X", "Y"}.issubset(df.columns):
                df["H"] = np.sqrt(df["X"]**2 + df["Y"]**2)

        else:
            columns = {
                f"{code}H": "H",
                f"{code}D": "D",
                f"{code}Z": "Z",
                f"{code}F": "F",
            }
            df = df.rename(columns=columns)

            if {"H", "D"}.issubset(df.columns):
                df["Y"] = df["H"] * np.sin(np.deg2rad(df["D"]))
                df["X"] = df["H"] * np.cos(np.deg2rad(df["D"]))

        return df


def dtrend(df, component="H", window=10, limit=200, center=False):
    """
    Remove running mean from selected component.

    Parameters
    ----------
    df : pandas.DataFrame
    component : str
        Magnetic component to detrend.
    window : int
        Rolling window size in samples.
    limit : float or None
        If given, clip detrended values outside [-limit, limit] to NaN.
    center : bool
        Whether rolling mean is centered.
    """
    out = df.copy()

    out["dtrend"] = out[component] - out[component].rolling(
        window=window, center=center
    ).mean()

    out["time"] = out.index.hour + out.index.minute / 60.0

    if limit is not None:
        out["dtrend"] = out["dtrend"].where(
            out["dtrend"].between(-limit, limit)
            )

    out = out.dropna(subset=["dtrend"])
    return out

infile = 'magnet/data/2025/TTB/ttb20250101qmin.min'
mg = Intermagnet(infile)

df = mg.dataframe 

df['Y'].plot()