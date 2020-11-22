import pandas as pd
import numpy as np
from typing import Union
from ._base import BaseTransformer

class DateComponents(BaseTransformer):

    def __init__(self, x : Union[str,list], components = {'year':'_YEAR','month':'_MONTH','day':'_DAY'}):
        super(DateComponents, self).__init__(x)
        self._components = components
        
    def fit(self, df):
        if self._fitted: return
        self._fitted = True
        
    def transform(self, df, in_place = False):
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        for z in self._x:
            if 'year' in self._components.keys():
                pf = self._components['year']
                df.loc[:,z+pf] = df[z].dt.year
            if 'month' in self._components.keys():
                pf = self._components['month']
                df.loc[:,z+pf] = df[z].dt.month
            if 'day' in self._components.keys():
                pf = self._components['day']
                df.loc[:,z+pf] = df[z].dt.day
        if not in_place: return(df)