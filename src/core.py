import os
import pandas as pd
import magnet as mg 

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

# df = mg.electrojet(c1 = 'slz', c2 = 'eus')

# df.plot()
