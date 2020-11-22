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
        self._map = None
        self._other_val = None
        
    def transform(self, df, in_place = False):
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        for z in self._x:
            df.loc[-df[z].isna(),z] = df.loc[-df[z].isna(),z] \
                .map(self._map).fillna(self._other_val)
        if not in_place: return(df)
        
#     def fit_transform(self, df, in_place = False):
#         self.fit(df)
#         self.transform(df, in_place)

        
class MaxLevelBinner(_CategoricalBinner):

    def __init__(self, x: Union[str,list], max_levels = 20, other_val = '_OTHER_'):
        super(MaxLevelBinner, self).__init__(x)
        self._max_levels = max_levels
        self._other_val = other_val
        
    def fit(self, df):
        if self._fitted: return
        for z in self._x:
            cnts = df.groupby(z).size() \
                     .sort_values(ascending = False) \
                     .head(self._max_levels)
            levels = cnts.index.tolist()
            self._map = {l:l for l in levels}
        self._fitted = True

        
class PercentThresholdBinner(_CategoricalBinner):
    
    def __init__(self, x: Union[str,list], percent_threshold = 0.02, other_val = '_OTHER_'):
        super(PercentThresholdBinner, self).__init__(x)
        self._percent_threshold = percent_threshold
        self._other_val = other_val
        
    def fit(self, df):
        if self._fitted: return
        for z in self._x:
            cnts = (df.groupby(z).size() / df.shape[0])
            levels = cnts[cnts>=self._percent_threshold].index.tolist()
            self._map = {l:l for l in levels}
        self._fitted = True
        
        
class CumulativePercentThresholdBinner(_CategoricalBinner):
    
    def __init__(self, x: Union[str,list], cum_percent = 0.95, other_val = '_OTHER_'):
        super(CumulativePercentThresholdBinner, self).__init__(x)
        self._cum_percent = cum_percent
        self._other_val = other_val
        
    def fit(self, df, x: Union[str,list]):
        if self._fitted: return
        for z in self._x:
            cnts = (df.groupby(z).size() / df.shape[0]) \
                      .sort_values(ascending=False).cumsum()
            levels = cnts[cnts<=self._cum_percent].index.tolist()
            self._map = {l:l for l in levels}
        self._fitted = True