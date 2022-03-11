# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 20:17:57 2022

@author: LuizF
"""

from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
import os.path
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from MagnetometersAnalysis import *


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    '''
    Nint
    The order of the filter.
    
    Wn array_like
    The critical frequency or frequencies. For lowpass and highpass 
    filters, Wn is a scalar; for bandpass and bandstop filters, Wn 
    is a length-2 sequence.
    
    For a Butterworth filter, this is the point at which the gain drops 
    to 1/sqrt(2) that of the passband (the “-3 dB point”).
    
    For digital filters, if fs is not specified, Wn units 
    are normalized from 0 to 1, where 1 is the Nyquist frequency 
    (Wn is thus in half cycles / sample and defined as 2*critical 
    frequencies / fs). If fs is specified, Wn is in the same units as fs.
    
    For analog filters, Wn is an angular frequency (e.g. rad/s).
    
    btype{‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, optional
    The type of filter. Default is ‘lowpass’.
    
    analogbool, optional
    When True, return an analog filter, otherwise a digital 
    filter is returned.
    
    output{‘ba’, ‘zpk’, ‘sos’}, optional
    Type of output: numerator/denominator (‘ba’), 
    pole-zero (‘zpk’), or second-order sections (‘sos’). 
    Default is ‘ba’ for backwards compatibility, but ‘sos’ s
    hould be used for general-purpose filtering.
    
    fs float, optional
    The sampling frequency of the digital system.

    
    '''
    if highcut == None:
        b, a = butter(order, lowcut, fs=fs, btype='lowpass')
    elif lowcut == None:
        b, a = butter(order, highcut, fs=fs, btype='highpass')
    else:
        b, a = butter(order, [lowcut, highcut], fs=fs, btype='bandpass')

    y = lfilter(b, a, data)
    return y

infile = 'G:\\My Drive\\Python\\doctorate-master\\AtmospherePhysics\\'\
    'Database\\Magnetometers\\Magnetometer15012022\\'

_, _, files = next(os.walk(infile))
filename = files[0]

df = setting_dataframe(infile, filename)

y = df['dtrend'].values
t = df['time'].values

#sample rate (frequency sampling)
fs = 1 / np.mean(np.diff(t))

lowcut = 1.5
highcut = None

filtered = butter_bandpass_filter(y, lowcut, highcut, fs = fs, order = 3)

fig, ax = plt.subplots(figsize = (12, 4), ncols = 2)

ax[0].plot(t, filtered, color = 'k', label='Filtered signal')
ax[0].plot(t, y, label='original')

ax[0].legend(loc = 'upper left')
ax[0].set(title = '')

ls = LombScargle(t, filtered, normalization='standard')

#95% of significace
fap = ls.false_alarm_level([0.5]) 

#filter the maxium periods
maximum_period = 30
minimum_period = 0.1
frequency, power = ls.autopower(minimum_frequency = (1 / maximum_period), 
                                maximum_frequency = (1 / minimum_period),
                                samples_per_peak = 100)

#plot the power in function of period
ax[1].plot((1 / frequency), power, lw = 1, color = 'black') 

#Plot false alarm probability
ax[1].axhline(fap, linestyle = ':', color = 'black', label = '95%')
plt.legend(loc = 'upper left')
ax[1].set( ylabel = 'PSD', xlabel = 'period (hours)')


