import matplotlib.pyplot as plt
import pandas as pd
import os
from common import load_by_time


def contour_map(df):
    ds = pd.pivot_table(
        df, 
        columns = df.index.date, 
        index = 'time', 
        values = 'F'
        )
    
    
    img = plt.contourf(ds.columns, 
                 ds.index,
                 ds.values)
    
    plt.colorbar(img)