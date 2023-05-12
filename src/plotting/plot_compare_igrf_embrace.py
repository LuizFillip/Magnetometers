from GEO import sites, year_fraction
import pyIGRF
import matplotlib.pyplot as plt
import settings as s

infile = "database/magnetometers/slz29jan.13m"

df = setting_dataframe(infile, component = 'H(nT)', N = 10)

site = "saa"
lat, lon = sites[site]["coords"]
    
d, i, h, x, y, z, f = pyIGRF.igrf_value(
    lat, 
    lon, 
    alt = 0, 
    year = year_fraction(df.index[0])
    )


def plot_compare_igrf_embrace():
    
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