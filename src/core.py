import os
import magnetometers as mm
import pandas as pd
from common import load_by_time

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
    
    df = df[~df.index.duplicated()] 
    return df.resample(freq).asfreq()

# infile = 'database/magnetometers/mag2.txt'


# df = load_by_time(infile)

# df = load_mag()

# df