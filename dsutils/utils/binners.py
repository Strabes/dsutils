import numpy as np
import math
import pandas as pd
import os
from decimal import Decimal
from .dates import bin_dates

def cutpoints(
    x,
    qntl_cutoff = [0.025,0.975],
    cuts = 'linear',
    ncuts = 10,
    sig_fig = 3,
    **kwargs):
    '''
    Function to return cut points and bin labels for a numeric 1-D array
    
    Parameters
    -----------------------------------------------
    x : numpy 1-D array
        numeric 1-D array
    
    qntl_cutoff : list
        list of length two with lower and upper quantile cutoffs:
        To prevent extreme outliers from influencing the cutpoints
        for the bins, construct the cutpoints between the qntl_cutoff[0] quantile
        and the qntl_cutoff[1] quantile. If qntl_cutoff is None then do not
        ignore outliers
        
    cuts: str
        one of: 'linear', 'log', 'logp1', 'quantile'
        'linear' : equally spaced cutpoints
        'log' : logarithmically spaced cutpoints
        'logp1' : logarithmically spaced cutpoints after adding 1
        'quantile' : cutpoints corresponding to equally spaced quantiles
        
    ncut : int
        number of cutpoints
    
    sig_fig : int
        number of significant figures to display in the aesthetically
        printed bin labels
        
    Returns
    -----------------------------------------------
    c_final : numpy 1-D array
        final cut points
    '''
    
    def log_spcl(x):
        if x == 0:
            return(0)
        else:
            return(math.log(abs(x),10))
    
    # Create lower bound:
    lb = np.min(x)
    if lb == 0:
        lb_ord_of_mag = 0
    else:
        lb_ord_of_mag = int(np.floor(log_spcl(lb)))
    lb_pwr = sig_fig - 1 - lb_ord_of_mag
    lb = np.floor(lb * 10**lb_pwr) / 10**lb_pwr
    # Create upper bound:
    ub = np.max(x)
    if ub == 0:
        ub_ord_of_mag = 0
    else:
        ub_ord_of_mag = int(np.floor(log_spcl(ub)))
    ub_pwr = sig_fig - 1 - ub_ord_of_mag
    ub = np.ceil(ub * 10**ub_pwr) / 10**ub_pwr
    
    # Apply quantile cutoffs if provided:
    if (qntl_cutoff is not None and
            len(qntl_cutoff) == 2 and
            isinstance(qntl_cutoff[0],float) and
            isinstance(qntl_cutoff[1],float)):
        ep = np.quantile(x, qntl_cutoff)
    else:
        ep = np.array([lb,ub])
        
    # Create cut points
    if isinstance(cuts,str):
        if cuts == 'linear':
            c = np.linspace(ep[0],ep[1],num = ncuts)
        elif cuts == 'log':
            if ep[0] == 0 or ep[1] == 0:
                msg = "Variable range includes zero when using 'log'" + \
                      " - consider using 'logp1' instead"
                raise ValueError(msg)
            else:
                c = 10**np.linspace(
                    np.sign(ep[0])*math.log(abs(ep[0]),10),
                    np.sign(ep[1])*math.log(abs(ep[1]),10),
                    num = ncuts
                    )
        elif cuts == 'logp1':
            c = 10**np.linspace(
                np.sign(ep[0])*math.log(abs(ep[0]) + 1,10),
                np.sign(ep[1])*math.log(abs(ep[1]) + 1,10),
                num = ncuts
                )
            c = np.sort(np.unique(np.append(0,c)))
        elif cuts == 'quantile':
            c = np.quantile(x,np.linspace(0,1,ncuts))
    else:
        # cuts are the actual cut points themselves
        c = cuts

    # add far endpoints to c:
    c = np.unique(np.append(np.append(lb,c),ub))
    # round/format values in c:
    c_ord_of_mag = np.array([int(np.floor(log_spcl(i))) for i in c])
    c_log_rnd = np.round(c / 10.0**c_ord_of_mag,sig_fig - 1)
    c_final = np.unique(c_log_rnd * (10.0**c_ord_of_mag))
    return(c_final)


def human_readable_num(number, sig_fig = 3, **kwargs):
    '''
    Function for making numbers aesthetically-pleasing
    
    Parameters
    -----------------------------------------------------
    number : a number to format
    
    sig_fig : number of significant figures to print
    
    Returns
    -----------------------------------------------------
    z : number formatted as str
    '''
    if number == 0:
        z = '0'
    elif np.abs(number) < 1:
        magnitude = int(math.floor(math.log(np.abs(number), 10)))
        # if |number| >= 0.01
        if magnitude >= -2:
            z = ('%.' + str(sig_fig - 1 - magnitude) + 'f') % (number)
        else:    
            final_num = number / 10**magnitude
            z = ('%.' + str(sig_fig - 1) + 'f%s') % (final_num, 'E' + str(magnitude))
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
            z = ('%.' + str(sig_fig - 1) + 'f%s') % (final_num, unit)
        elif np.abs(final_num) < 100:
            z = ('%.' + str(sig_fig-2) + 'f%s') % (final_num, unit)
        else:
            z = ('%.' + str(sig_fig-3) + 'f%s') % (final_num, unit)
    return(z)


def cutter(df, x, max_levels = 20, point_mass_threshold = 0.1, sig_fig = 3, **kwargs):
    """
    Cut a numeric variable into bins
    
    Parameters
    --------------------------
    df : pandas DataFrame object
    
    x : the name of the numeric variable in 'df' to construct bins from
    
    max_levels : maximum number of bins to create from 'x'
    
    Returns
    ---------------------------
    z : binned values
    """
    
    df = df.loc[:,[x]].copy()
    
    # pm contains any values that exceed point_mass_threshold
    # pm is 1-D numpy.array
    cnts = df.groupby(x).size().sort_values(ascending=False)
    cnts = cnts / cnts.sum()
    pm = cnts[cnts > point_mass_threshold].index.values
    pm.sort()
    
    if len(pm) == 0:
        # if there are no values exceeding point_mass_threshold
        # proceed as usual
        x_no_nan = ~np.isnan(df.loc[:,x].values)
        c_final = cutpoints(
            df.loc[x_no_nan,x].values,
            ncuts = max_levels,
            **kwargs)
        c_format = [human_readable_num(i, sig_fig) for i in c_final]
        pm_format = []
        
    elif len(pm) > 0:
        # if there are values exceeding point_mass_threshold
        # put all remaining values in rem
        rem = df.loc[~df[x].isin(pm),[x]]
        x_no_nan = ~np.isnan(rem.loc[:,x].values)
        if len(rem.loc[x_no_nan,x].values) > 0:
            # apply cutpoints to rem if there are non-NaN
            # values
            c_final = cutpoints(
                rem.loc[x_no_nan,x].values,
                ncuts = max_levels - len(pm),
                **kwargs)
            c_format = [human_readable_num(i, sig_fig) for i in c_final]
        else:
            # Otherwise, rem has no non-NaN values and
            # we just generate empty cutpoints and formatted numbers
            c_final, c_format = np.array([]), []
        # Combine pm and c_final
        # Combine pm_format and c_format
        pm_format = [human_readable_num(i, sig_fig) for i in pm]
        c_final = np.concatenate([c_final,pm])
        c_format = c_format + pm_format
        c_format = [x for _,x in sorted(zip(c_final.tolist(),c_format))]
        c_final.sort()

    # Construct bin_labels and pm_labels
    bin_labels = []
    pm_labels = []
    cntr = 0
    for i in range(len(c_final)):
        if c_final[i] in pm:
            pm_labels.append(str(i+cntr+1).zfill(2) + ": " + c_format[i])
            cntr+=1
        if i < len(c_final) - 1:
            bin_labels.append(
                str(i + cntr +1).zfill(2) +
                ': ' +
                c_format[i] +
                ' - ' +
                c_format[i+1])

    df.loc[~df[x].isin(pm),x + '_BINNED'] = pd.cut(
        df.loc[~df[x].isin(pm),x].values,
        c_final,
        labels=bin_labels,
        include_lowest=True)
    for i,v in enumerate(pm):
        df.loc[df[x] == v,x + '_BINNED'] = pm_labels[i]
    z = df.loc[:,x + '_BINNED'].values
    return(z)


def binner_df(df, x, new_col, fill_nan = None, max_levels = 20, **kwargs):
    """
    Bin a numeric variable
    
    Parameters
    --------------------------
    df : pandas DataFrame object
    
    x : the name of the numeric variable in 'df' to construct bins from
    
    new_col : str to use as the name of the binned variable
    
    fill_nan : string to fill nan values
    
    max_levels : maximum number of bins to create from 'x'
    
    Returns
    ---------------------------
    df_ : pandas DataFrame including new binned column
    """
    df_ = df.copy().assign(**{new_col : lambda z: cutter(z,x,max_levels,**kwargs)})
    if fill_na is not None:
        df_.replace({new_col:{np.nan:fill_na}})
    return(df_)
