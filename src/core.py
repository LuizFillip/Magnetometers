import os
import magnetometers as mm
import pandas as pd

def concat_files(infile):
    out = []
    for filename in os.listdir(infile):
        out.append(
            mm.load(os.path.join(infile, filename))
            )
    return pd.concat(out)


def main():

    infile = "database/magnetometers/2013/"
    
    df = concat_files(infile)
    
    df.to_csv("database/magnetometers/mag2.txt")
    

def load_mag(
        infile = "database/magnetometers/mag2.txt",
        freq = "10min"
        ):

    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
        
    df["F"] = df["F"] * 1e-9
    
    #df = df[~df.index.duplicated()] 
    return df.sort_index() #df.resample(freq).asfreq()

def test():
    import datetime as dt
    mag = load_mag()
   # 2013-05-11 20:00:00
    dn = dt.datetime(2013, 5, 11, 20, )
    B = mag[mag.index == dn]['F']
    #print(mag['F'].mean())
