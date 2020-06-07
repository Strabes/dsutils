import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import os
from decimal import Decimal

def numericVarCutpoints(
    x,
    qntlCutoff = [0.025,0.975],
    cuts = 'linear',
    ncuts = 10,
    sigFig=3,
    **kwargs):
    '''
    Function to return cut points and bin labels for a numeric 1-D array
    
    Parameters
    -----------------------------------------------
    x : numeric 1-D array
    
    qntlCutoff : to prevent extreme outliers from influencing the cutpoints
        for the bins, construct the cutpoints between the qntlCutoff[0] quantile
        and the qntlCutoff[1] quantile. If qntlCutoff is None then do not
        ignore outliers
        
    cuts: 'linear', 'log', 'quantile'
        'linear' : equally spaced cutpoints
        'log' : logarithmically spaced cutpoints
        'quantile' : cutpoints corresponding to equally spaced quantiles
        
    ncut : number of cutpoints
    
    sigFig : number of significant figures to display in the aesthetically
        printed bin labels
        
    Returns
    -----------------------------------------------
    list containing :
        c_final : numpy 1-D array of final cut points
        c_format : list of aesthetically-pleasing cut point labels
    '''
    # Create lower bound:
    lb = np.min(x)
    lb_ordOfMag = int(np.floor(math.log(abs(lb),10)))
    lb = np.floor(lb * 10**(sigFig - 1 - lb_ordOfMag)) / 10**(sigFig - 1 - lb_ordOfMag)
    # Create upper bound:
    ub = np.max(x)
    ub_ordOfMag = int(np.floor(math.log(abs(ub),10)))
    ub = np.ceil(ub * 10**(sigFig - 1 - ub_ordOfMag)) / 10**(sigFig - 1 - ub_ordOfMag)
    if (qntlCutoff is not None and
            len(qntlCutoff) == 2 and
            isinstance(qntlCutoff[0],float) and
            isinstance(qntlCutoff[1],float)):
        ep = np.quantile(x, qntlCutoff)
    else:
        ep = np.array([lb,ub])
    if isinstance(cuts,str):
        if cuts == 'linear':
            c = np.linspace(ep[0],ep[1],num = ncuts)
        elif cuts == 'log':
            c = 10**np.linspace(
                np.sign(ep[0])*math.log(abs(ep[0]),10),
                np.sign(ep[1])*math.log(abs(ep[1]),10),
                num = ncuts
                )
        elif cuts == 'quantile':
            c = np.quantile(x,np.linspace(0,1,10))
    else:
        # cuts are the actual cut points themselves
        c = cuts

    # add far endpoints to c:
    c = np.unique(np.append(np.append(lb,c),ub))
    # round/format values in c:
    c_abs = abs(c)
    c_ordOfMag = np.array([int(np.floor(math.log(i,10))) for i in c_abs])
    c_log_rnd = np.round(c / 10.0**c_ordOfMag,2)
    c_final = np.unique(c_log_rnd * (10.0**c_ordOfMag))
    units = ['', 'K', 'M', 'G', 'T', 'P']
    #c_format = ['%.2f%s' % (i, units[j]) for i,j in zip(c_log_rnd,c_ordOfMag//4)]
    c_format = [humanReadableNum(i, sigFig = sigFig) for i in c_final]
    return([c_final,c_format])
    
    
    
def humanReadableNum(number,sigFig = 3):
    '''
    Function for making numbers aesthetically-pleasing
    
    Parameters
    -----------------------------------------------------
    number : a number to format
    
    sigFig : number of significant figures to print
    
    Returns
    -----------------------------------------------------
    z : number formatted as str
    '''
    if np.abs(number) < 1:
        magnitude = int(math.floor(math.log(np.abs(number), 10)))
        # if |number| >= 0.01
        if magnitude >= -2:
            z = ('%.' + str(sigFig - 1 - magnitude) + 'f') % (number)
        else:    
            final_num = number / 10**magnitude
            z = ('%.' + str(sigFig - 1) + 'f%s') % (final_num, 'E' + str(magnitude))
    else:
        units = ['', 'K', 'M', 'G', 'T', 'P']
        k = 1000.0
        magnitude = int(math.floor(math.log(np.abs(number), k)))
        final_num = number / k**magnitude
        if magnitude > 5:
            unit = 'E' + str(int(3*magnitude))
        else:
            unit = units[magnitude]
        if np.abs(final_num) < 10:
            z = ('%.' + str(sigFig - 1) + 'f%s') % (final_num, unit)
        elif np.abs(final_num) < 100:
            z = ('%.' + str(sigFig-2) + 'f%s') % (final_num, unit)
        else:
            z = ('%.' + str(sigFig-3) + 'f%s') % (final_num, unit)
    return(z)



def plotBar(p,
            x = 'x',
            line_columns = None,
            bar_color = 'xkcd:light blue',
            line_colors = ['xkcd:red','orange','b','y','g','c','m'],
            **kwargs):
    '''
    Function for creating a bar plot for categorical data.
    If input pandas DataFrame include a column with name 'response',
    this function also plots a line with these values.
    By passing a matplotlib figure, 'fig', and axis object, 'ax',
    this function can add the plot to the provided axis
    
    Parameters
    --------------------------
    p : pandas DataFrame object that contains:
        x : the categorical variable to plot along the x-axis
        Count : the height of the bars
        line_columns : optional list of columns to plot as lines

    x : the categorical variable in 'df' to plot along the x-axis

    line_columns : optional list of columns to plot as lines
        
    bar_color : a color for the bars, must be recognized by matplotlib
    
    line_colors : colors for the lines, must be recognized by matplotlib
    
    **kwargs : optional parameters:
        fig : a matplotlib figure
        ax : a matplotlib axis object
        
    Returns
    ---------------------------
    fig : a matplotlib figure
    '''
    if 'fig' in kwargs.keys() and 'ax' in kwargs.keys():
        fig = kwargs['fig']; ax = kwargs['ax']
    else:
        fig = plt.figure()
        ax = plt.gca()
        
    n = p.shape[0]
    _ = ax.bar(
        range(n),
        p.loc[:,'Count'],
        color = bar_color,
        align='center',
        width=0.9
    )
    ax.set_xticks(range(n))
    ax.set_xticklabels(
        p.loc[:,x].values.tolist(),
        rotation=45,ha='right')
    if line_columns is not None:
        twinx = ax.twinx()
        if isinstance(line_columns,str):
            line_columns = [line_columns]
        for i, col in enumerate(line_columns):
            _ = twinx.plot(
                range(n),
                p.loc[:,col],
                color = line_colors[i]
            )
        twinx.spines['top'].set_visible(False)
        if 'ylabel' in kwargs:
            plt.ylabel(kwargs['ylabel'], labelpad = 15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.sca(ax)
    plt.ylabel('Count')
    if 'xlabel' in kwargs:
        plt.xlabel(kwargs['xlabel'])
    return(fig)


def _numericHistogram(
    df,
    x = 'x',
    oth_columns = None,
    max_levels = 20,
    stat = 'mean',
    **kwargs):
    '''
    Function for histogramming a numeric column into bins and
    optionally calculating statistics of other columns within
    these bins
    
    Parameters
    --------------------------
    df : pandas DataFrame object
    
    x : the name of the numeric variable in 'df' to construct bins from
    
    oth_columns : optional list of other columns in 'df' on which to
        calculate 'stat'
        
    max_levels : maximum number of bins to create from 'x'
    
    stat : aggregate statistic to calculate on 'oth_columns' within
        bins of 'x'
        
    Returns
    ---------------------------
    p : pandas DataFrame object
    '''
    if oth_columns is None:
        oth_columns = []
    elif isinstance(oth_columns,str):
        oth_columns = [oth_columns]
    
    x_no_nan = ~np.isnan(df.loc[:,x].values)
    f = numericVarCutpoints(df.loc[x_no_nan,x].values,**kwargs)
    labels = [(
        str(i+1).zfill(2) +
        ': ' +
        f[1][i] +
        ' - ' +
        f[1][i+1]) for i in range(len(f[1])-1)]
    
    x_grp = x + ' _GROUPED_'
    
    if len(oth_columns) > 0:
        stats = dict(zip(oth_columns,[stat]*len(oth_columns)))
    else:
        stats = dict()
    stats['Count'] = 'sum'
    p = (
        df[[*oth_columns,x]].copy()
        .assign(**{x_grp: lambda z: pd.cut(z.loc[:,x].values,f[0],labels=labels)})
        .replace({x_grp:{np.nan:'MISSING'}})
        .assign(Count = 1)
        .groupby(x_grp)
        .agg(stats)
        .reset_index()
        .rename(columns = {x_grp:x})
        )

    return(p)


def _categoricalHistogram(
    df,
    x = 'x',
    oth_columns = None,
    max_levels = 20,
    oth_val = '_OTHER_',
    stat = 'mean',
    **kwargs):
    '''
    Function for histogramming a categorical variable into bins and
    optionally calculating statistics of other columns within
    these bins
    
    Parameters
    --------------------------
    df : pandas DataFrame object
    
    x : the name of the categorical variable in 'df' to construct bins from
    
    oth_columns : optional list of other columns in 'df' on which to
        calculate 'stat'
        
    max_levels : maximum number of bins to create from 'x' - the max_level
        values of 'x' with the greatest record counts receive their own levels,
        all other levels are binned as 'oth_val'
        
    oth_val : str used as value for levels with fewer record counts
    
    stat : aggregate statistic to calculate on 'oth_columns' within
        bins of 'x'
        
    Returns
    ---------------------------
    p : pandas DataFrame object
    '''

    if oth_columns is None:
        oth_columns = []
    elif isinstance(oth_columns,str):
        oth_columns = [oth_columns]
    
    x_grp = x + ' _GROUPED_'
    k = {x_grp: lambda z: z.apply(lambda f: f[x] if f.RN <= max_levels else oth_val, axis = 1)}
    cnts = (
        df.groupby(x)
          .size()
          .to_frame(name='Count')
          .reset_index()
          .sort_values('Count',ascending = False)
          .assign(RN = lambda x: x['Count'].rank(method = 'first',ascending = False))
          .assign(**k)
        )
    m = dict(zip(cnts[x],cnts[x_grp]))
    if len(oth_columns) > 0:
        stats = dict(zip(oth_columns,[stat]*len(oth_columns)))
    else:
        stats = dict()
    stats['Count'] = 'sum'
    p = (
        df.assign(**{x_grp: lambda f: f[x].map(m)})
          .assign(Count = 1)
          .groupby(x_grp)
          .agg(stats)
          .reset_index()
          .rename(columns = {x_grp:x})
    )
    return(p)

def numericHistogram(
    df,
    x = 'x',
    line_columns = None,
    max_levels = 20,
    bar_color = 'xkcd:light blue',
    line_colors = ['xkcd:red','orange','b','y','g','c','m'],
    stat = 'mean',
    **kwargs):
    '''
    Function to create matplotlib histogram plot
    
    Parameters
    --------------------------
    df : pandas DataFrame object
    
    x : the name of the numeric variable in 'df' to construct bins from
    
    line_columns : optional list of other columns in 'df' on which to
        calculate and plot 'stat' within bins of 'x'
        
    max_levels : maximum number of bins to create from 'x'
    
    bar_color : color for bars - must be recognized by matplotlib
    
    line_colors : list of colors for line, if any - must be
        recognized by matplotlib
    
    stat : aggregate statistic to calculate on 'oth_columns' within
        bins of 'x'
        
    Returns
    ---------------------------
    p : matplotlib figure

    
    '''
    p = _numericHistogram(
        df,
        x = x,
        oth_columns = line_columns,
        max_levels = max_levels,
        stat = stat,
        **kwargs)
    p = plotBar(p,
            x = x,
            line_columns = line_columns,
            bar_color = bar_color,
            line_colors = line_colors,
            **kwargs)
    return(p)


def categoricalHistogram(
    df,
    x = 'x',
    line_columns = None,
    max_levels = 20,
    oth_val = '_OTHER_',
    bar_color = 'xkcd:light blue',
    line_colors = ['xkcd:red','orange','b','y','g','c','m'],
    stat = 'mean',
    **kwargs):
    '''
    Function to create matplotlib histogram plot
    
    Parameters
    --------------------------
    df : pandas DataFrame object
    
    x : the name of the categorical variable in 'df' to construct bins from
    
    line_columns : optional list of other columns in 'df' on which to
        calculate and plot 'stat'
        
    max_levels : maximum number of bins to create from 'x' - the max_level
        values of 'x' with the greatest record counts receive their own levels,
        all other levels are binned as 'oth_val'
        
    oth_val : str used as value for levels with fewer record counts
    
    bar_color : color for bars - must be recognized by matplotlib
    
    line_colors : list of colors for line, if any - must be
        recognized by matplotlib
    
    stat : aggregate statistic to calculate on 'oth_columns' within
        bins of 'x'
        
    Returns
    ---------------------------
    p : matplotlib figure
    '''

    p = _categoricalHistogram(
        df,
        x = x,
        oth_columns = line_columns,
        max_levels = max_levels,
        oth_val = oth_val,
        stat = stat,
        **kwargs)
    p = plotBar(p,
            x = x,
            line_columns = line_columns,
            bar_color = bar_color,
            line_colors = line_colors,
            **kwargs)
    return(p)