from astropy.timeseries import LombScargle


def plot_LombScargle(t, y, ax = None, 
                     minimum_period = 0.3, 
                     maximum_period = 2):    
    
    '''
    Compute and plot the Lomb-Scargle periodogram (Astropy library)
    '''
        
    #compute the periodogram and false alarm probability 
    ls = LombScargle(t, y, normalization='standard')
    #95% of significance level
    fap = ls.false_alarm_level([0.5]) 
    #Compute 
    frequency, power = ls.autopower(minimum_frequency = (1 / maximum_period), 
                                    maximum_frequency = (1 / minimum_period), 
                                    samples_per_peak = 100)
    
    # Compute the period (inverse of frequency)
    period = (1 / frequency)
    
    if ax:
        ax.plot(period, power, lw = 1, color = 'black') 
        
        #Plot false alarm probability
        ax.axhline(fap, linestyle = ':', color = 'black', 
                   label = 'Confidence 95%')
        
    return period, power

        
