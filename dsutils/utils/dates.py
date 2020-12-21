"""
Date utilities
"""

import pandas as pd
import numpy as np

def bin_dates(d, bins, midpoint=True):
    """
    Bin a 1d-array-like of datetimes
    
    Parameters
    ----------
    d : 1D array-like of datetimes
    
    bins : int or 1D array-like of datetimes
    
    midpoint : Boolean
        if True, use midpoints of bins as labels
        if False, use bins from pandas.cuts as labels
        
    Returns
    -------
    pandas.Series of binned dates
    """
    if not pd.api.types.is_datetime64_any_dtype(d):
        raise(TypeError("d must be of type datetime64"))
    if isinstance(bins,int):
        z, bins = pd.cut(d,bins,retbins=True)
        bins = [pd.to_datetime(s.date()) for s in bins.tolist()]
        bins[-1] = c[-1] + pd.DateOffset(1)
        
    if midpoints:
        m = [(bins[i-1] + (bins[i] - bins[i-1])/2).date() for i in range(1,len(bins))]
        d = pd.cut(d,bins,labels=m)
    else:
        d = pd.cut(d,bins)
        
    return(d)