import numpy as np
import pandas as pd
from typing import Union

from ._base import BaseTransformer

class OutlierPercentileCapper(BaseTransformer):
    
    def __init__(self, x = Union[str,list], percentiles = [0.01,0.99]):
        super(OutlierPercentileCapper, self).__init__(x)
        self._percentiles = percentiles
        self._map = {}
        
    def fit(self, df):
        if self._fitted: return
        for z in self._x:
            vals = df[z].quantile(self._percentiles).values
            self._map = {z: vals}
        self._fitted = True
        
    def transform(self, df, in_place = False):
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        for z in self._x:
            vals = self._map[z]
            df.loc[df[z] < vals[0],z] = vals[0]
            df.loc[df[z] > vals[1],z] = vals[1]
        if not in_place: return(df)