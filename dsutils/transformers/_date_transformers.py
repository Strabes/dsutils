import pandas as pd
import numpy as np
from typing import Union
from ._base import BaseTransformer

class DateComponents(BaseTransformer):

    def __init__(self, variables : Union[str,list],
                 components = {'year':'_YEAR','month':'_MONTH','day':'_DAY'}):
        super(DateComponents, self).__init__(variables)
        self.components = components
        
    def fit(self, X, y = None):
        if self.fitted: return
        self.fitted = True
        
    def transform(self, X):
        if not self.fitted:
            raise Exception("Transformation not fit yet")
        X = X.copy()
        for z in self.variables:
            if 'year' in self.components.keys():
                pf = self.components['year']
                X.loc[:,z+pf] = X[z].dt.year
            if 'month' in self.components.keys():
                pf = self.components['month']
                X.loc[:,z+pf] = X[z].dt.month
            if 'day' in self.components.keys():
                pf = self.components['day']
                X.loc[:,z+pf] = X[z].dt.day
        return X