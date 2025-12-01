import os
import pandas as pd
import magnet as mg 

df = mg.electrojet(c1 = 'slz', c2 = 'eus')

df.plot()
