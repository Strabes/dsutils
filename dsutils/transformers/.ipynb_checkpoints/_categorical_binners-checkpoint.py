import pandas as pd
import numpy as np
from typing import Union
from ._base import BaseTransformer

class _CategoricalBinner(BaseTransformer):
    """
    Base class for all categorical binnning transformers
    """
    def __init__(self, x = Union[str,list]):
        super(_CategoricalBinner, self).__init__(x)
        self._map = {}
        self._other_val = None
        
    def transform(self, df, in_place = False):
        """
        Default transform method
        
        Parameters
        ----------
        df : pandas.DataFrame
        
        in_place : Boolean
        
        Returns
        -------
        None if in_place is True
        pandas.DataFrame if in_place is False
        """
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        for z in self._x:
            df.loc[-df[z].isna(),z] = df.loc[-df[z].isna(),z] \
                .map(self._map[z]).fillna(self._other_val)
        if not in_place: return(df)

        
class MaxLevelBinner(_CategoricalBinner):
    """
    MaxLevelBinner
    """
    def __init__(self, x: Union[str,list], max_levels = 20, other_val = '_OTHER_'):
        super(MaxLevelBinner, self).__init__(x)
        self._max_levels = max_levels
        self._other_val = other_val
        
    def fit(self, df):
        """
        Fit method
        
        Parameters
        ----------
        df : pandas.DataFrame
        """
        if self._fitted: return
        for z in self._x:
            cnts = df.groupby(z,dropna=False).size() \
                     .sort_values(ascending = False) \
                     .head(self._max_levels)
            levels = cnts.index.tolist()
            self._map[z] = {l:l for l in levels}
        self._fitted = True

        
class PercentThresholdBinner(_CategoricalBinner):
    """
    PercentThresholdBinner
    """
    def __init__(self, x: Union[str,list], percent_threshold = 0.02, other_val = '_OTHER_'):
        super(PercentThresholdBinner, self).__init__(x)
        self._percent_threshold = percent_threshold
        self._other_val = other_val
        
    def fit(self, df):
        """
        Fit method
        
        Parameters
        ----------
        df : pandas.DataFrame
        """
        if self._fitted: return
        for z in self._x:
            cnts = (df.groupby(z,dropna=False).size() / df.shape[0])
            levels = cnts[cnts>=self._percent_threshold].index.tolist()
            self._map[z] = {l:l for l in levels}
        self._fitted = True
        
        
class CumulativePercentThresholdBinner(_CategoricalBinner):
    """
    CumulativePercentThresholdBinner
    """
    def __init__(self, x: Union[str,list], cum_percent = 0.95, other_val = '_OTHER_'):
        super(CumulativePercentThresholdBinner, self).__init__(x)
        self._cum_percent = cum_percent
        self._other_val = other_val
        
    def fit(self, df):
        """
        Fit method
        
        Parameters
        ----------
        df : pandas.DataFrame
        """
        if self._fitted: return
        for z in self._x:
            cnts = (df.groupby(z,dropna=False).size() / df.shape[0]) \
                      .to_frame(name = z + '_perc').reset_index() \
                      .sort_values([z + '_perc',z], ascending = [False,True]) \
                      .set_index(z) \
                      .cumsum().shift(periods=1, fill_value=0)
            levels = cnts[cnts[z + '_perc']<=0.85].index.tolist()
            self._map[z] = {l:l for l in levels}
        self._fitted = True