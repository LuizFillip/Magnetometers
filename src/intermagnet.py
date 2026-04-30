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
        drop_cols = [c for c in 
                     ["DATE", "TIME", "DOY", "|"] if 
                     c in df.columns]
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
                
        df = df.loc[~(df['H'] > 1e5)]
        return df

def inter_path(dn, code = 'ttb'):
    fn = dn.strftime(f'{code}%Y%m%dqmin.min')
    return f'magnet/data/{dn.year}/{code.upper()}/{fn}'

def load_intermag(dn, code):
    infile = inter_path(dn, code = code)
    
    return Intermagnet(infile).dataframe 

def test_inter_path():
    fn = 'ttb20250101qmin.min'
    
    dn = dt.datetime(2025, 1, 1)
    inter_path(dn, code = 'ttb')