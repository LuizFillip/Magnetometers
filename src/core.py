import os
import magnetometers as mm
import pandas as pd

def concat_files(infile):
    out = []
    for filename in os.listdir(infile):
        out.append(
            mm.load(infile + filename)
            )
    return pd.concat(out)


def main():

    infile = "database/magnetometers/201303/"
    
    df = concat_files(infile)
    
    df.to_csv("database/magnetometers/mag.txt")
    

def load_mag(infile = "database/magnetometers/mag.txt", freq = "10min"):

    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    df = df.resample(freq).asfreq()
    
    df["F"] = df["F"] * 1e-9
    return df
    