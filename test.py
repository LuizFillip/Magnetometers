# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 23:04:33 2022

@author: LuizF
"""

import pandas as pd
import random

index = pd.date_range(start = '2020-01-01 00:00:00', 
                         end = '2020-04-01 00:00:00', freq='5T')
s = pd.Series(index=index, dtype=np.float64 )
s = s.apply(lambda x: random.randint(1,20))
s=s[s.ne(1)]


print(s.index.to_series().diff().value_counts())

print(s.index.to_series().diff().median())