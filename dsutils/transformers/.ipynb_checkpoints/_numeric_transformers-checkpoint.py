import numpy as np
import pandas as pd
from typing import Union

from ._base import BaseTransformer

class OutlierPercentileCapper(BaseTransformer):
    
    def __init__(self, x = Union[str,list], lower = 0.01, upper = 0.99):
        super(OutlierPercentileCapper, self).__init__(x)
        self._lower = lower
        self._upper = upper
        self._map = {}
        
    def fit(self, df):
        if self._fitted: return
        for z in self._x:
            self._map[z] = {}
            if self._lower is not None:
                self._map[z]['lower'] = df[z].quantile(
                    self._lower)
            if self._upper is not None:
                self._map[z]['upper'] = df[z].quantile(
                    self._upper)
        self._fitted = True
        
    def transform(self, df, in_place = False):
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        for z in self._x:
            vals = self._map[z]
            if 'lower' in vals.keys():
                df.loc[df[z] < vals['lower'],z] = vals['lower']
            if 'upper' in vals.keys():
                df.loc[df[z] > vals['upper'],z] = vals['upper']
        if not in_place: return(df)