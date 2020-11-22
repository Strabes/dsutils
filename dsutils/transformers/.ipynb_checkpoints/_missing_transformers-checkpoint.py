import pandas as pd
import numpy as np
from typing import Union
from ._base import BaseTransformer


class MissingIndicator(BaseTransformer):
    def __init__(self, x: Union[str,list], postfix = "_NA_IND"):
        super(MissingIndicator, self).__init__(x)
        self._postfix = postfix
        
    def fit(self, df):
        if self._fitted: return
        self._fitted = True
        
    def transform(self, df, in_place = False):
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        postfix = self._postfix
        for z in self._x:
            df[z + postfix] = df[z].isna().astype(int)
        if not in_place: return(df)

class BaseMissingTransformer(BaseTransformer):
    
    def __init__(self, x: Union[str,list]):
        super(BaseMissingTransformer, self).__init__(x)
        self.fillna = {}
        
    def transform(self, df, in_place = False):
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        for z in self._x:
            df.loc[df[z].isna(),z] = self.fillna[z]
        if not in_place: return(df)

        
class ReplaceMissingMean(BaseMissingTransformer):
    
    def __init__(self,x: Union[str,list]):
        super(ReplaceMissingMean, self).__init__(x)
        
    def fit(self, df):
        if self._fitted: return
        for z in self._x:
            self.fillna[z] = df.loc[-df[z].isna(),z].mean()
        self._fitted = True
            
class ReplaceMissingMedian(BaseMissingTransformer):
    
    def __init__(self, x: Union[str,list]):
        super(ReplaceMissingMedian, self).__init__(x)
        
    def fit(self, df):
        if self._fitted: return
        for z in self._x:
            self.fillna[z] = df.loc[-df[z].isna(),z].median()
        self._fitted = True
            
class ReplaceMissingNumericConstant(BaseMissingTransformer):
    
    def __init__(self, x: Union[str,list], constant: Union[float,dict] = 0):
        super(ReplaceMissingNumericConstant, self).__init__(x)
        self.constant = constant
        
    def fit(self, df):
        if self._fitted: return
        for z in self._x:
            if isinstance(self.constant,dict):
                self.fillna[z] = self.constant[z]
            else:
                self.fillna[z] = self.constant
        self._fitted = True

class ReplaceMissingCategorical(BaseMissingTransformer):
    
    def __init__(self, x: Union[str,list], constant: Union[str,dict] = "_MISSING_"):
        super(ReplaceMissingCategorical, self).__init__(x)
        self.constant = constant
        
    def fit(self, df):
        if self._fitted: return
        for z in self._x:
            if isinstance(self.constant, dict):
                self.fillna[z] = self.constant[z]
            else:
                self.fillna[z] = self.constant
        self._fitted = True