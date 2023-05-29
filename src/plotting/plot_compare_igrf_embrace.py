from GEO import sites, year_fraction
import pyIGRF
import matplotlib.pyplot as plt
import settings as s
import magnetometers as mm
import os
import pandas as pd


def load_igrf(df, site = "saa"):
   
    lat, lon = sites[site]["coords"]
    
    out = {"D": [], "H": [], "Z": [], 
           "I": [], "F": [], "X": [], 
           "Y": []
           }
    for dn in df.index:
        D, I, H, X, Y, Z, F = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = 0, 
            year = year_fraction(dn)
            )
        
        for key in out.keys():
            out[key].append(vars()[key])
  
    return pd.DataFrame(out, index = df.index)


def plot_compare_igrf_embrace(df):
    
    f = load_igrf()
    
    fig, ax = plt.subplots(
        sharey = True,
        dpi = 300)
    
    ax.axhline(f, label = "IGRF-12")
    
    ax.plot(df["F(nT)"], label = "Embrace", color = "r")
    ax.legend()
    
    s.set_date_axis(ax)
    
    ax.set(ylabel = "F(nT)", 
           xlabel = "Hora universal", 
           title = df.index[0].date())
    
    
infile = "database/magnetometers/"

def concat_files(infile):
    out = []
    for filename in os.listdir(infile):
        out.append(
            mm.load(infile + filename)
            )
    return pd.concat(out)

df = concat_files(infile)
# df["F(nT)"].plot()

igr = load_igrf(df, site = "saa")

igr
#%%


def plot_comparece_igrf_embrace(df, igr):

    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 2, 
        figsize = (12, 8),
        dpi = 300,
        sharex = True
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.3)
    
    cols = ['D', 'I', 'H', 'F']
    name = ["Declinação", 'Inclinação', 
            'Horizonal', 'Total']
    
    lims = [[-21.3, -20.7],
            [-7.8, -7.3],
            [25900, 26200], 
            [26100, 26400]]
    c = s.chars()
    
    for i, ax in enumerate(ax.flat):
        
        ax.text(0.05, 0.85, f'({c[i]}) {name[i]}', 
                transform = ax.transAxes)
        ax.plot(df[cols[i]], label = "Magnetômetro - São Luis")
        ax.plot(igr[cols[i]], label = "IGRF-12", lw = 2)
        
        
        ax.set(ylim = lims[i])
        if i >= 2:
            s.format_time_axes(ax)
            ax.set(ylabel = f"{cols[i]} (nT)")
        else:
            ax.set(ylabel = f"{cols[i]} (°)")
            
        if i == 0:
            ax.legend(ncol = 2, 
                      bbox_to_anchor = (1.1, 1.25),
                      loc = "upper center")
    return fig
            
f = plot_comparece_igrf_embrace(df, igr)

f.savefig("magnetometers/figures/comparation_igrf_embrace.png", 
          dpi = 300)