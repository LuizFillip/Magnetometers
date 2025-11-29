import matplotlib.pyplot as plt 

def plot_electrojet_stages(days, code):
    fig, ax = plt.subplots(
        nrows= 3, 
        sharex = True, 
        # sharey = True, 
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    
    df = quiet_time(days, code= code)
    
    ax[0].plot(df)
     
    ax[0].plot(df.mean(axis = 1), lw = 4, color = 'k')
    
    qt = filter_and_avg(df)
    
    ax[1].fill_between(
        qt.index, 
        qt['h'] - qt['std'], 
        qt['h'] + qt['std'], 
        color = "red", 
        alpha = 0.3
        )
    
    ax[1].plot(qt['h'], color = 'red')
    
    ax[1].axvline(3, color = 'k', lw = 3, linestyle = '--')
    
    mid = qt.loc[qt.index == 3, 'h'].item()
    
    ax[2].plot(qt['h'] - mid, label = '$\delta H$ (vassouras)')

