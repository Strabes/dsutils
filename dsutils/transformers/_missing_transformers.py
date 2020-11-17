import pandas as pd
import numpy as np
from typing import Union
from ._base import BaseTransformer


class MissingIndicator(BaseTransformer):
    def __init__(self):
        super(MissingIndicator, self).__init__()
        
    def fit(self, df, x: Union[str,list], postfix = "_NA_IND"):
        if self._fitted: return
        if isinstance(x,str): x = [x]
        self._x = x
        self._postfix = postfix
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
    
    def __init__(self):
        super(BaseMissingTransformer, self).__init__()
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
    
    def __init__(self):
        super(ReplaceMissingMean, self).__init__()
        
    def fit(self, df, x: Union[str,list]):
        if self._fitted: return
        if isinstance(x,str): x = [x]
        self._x = x
        for z in self._x:
            self.fillna[z] = df.loc[-df[z].isna(),z].mean()
        self._fitted = True
            
class ReplaceMissingMedian(BaseMissingTransformer):
    
    def __init__(self):
        super(ReplaceMissingMedian, self).__init__()
        
    def fit(self, df, x: Union[str,list]):
        if self._fitted: return
        if isinstance(x,str): x = [x]
        self._x = x
        for z in self._x:
            self.fillna[z] = df.loc[-df[z].isna(),z].median()
        self._fitted = True
            
class ReplaceMissingNumericConstant(BaseMissingTransformer):
    
    def __init__(self, constant: Union[float,dict] = 0):
        super(ReplaceMissingNumericConstant, self).__init__()
        self.constant = constant
        
    def fit(self, df, x: Union[str,list]):
        if self._fitted: return
        if isinstance(x,str): x = [x]
        self._x = x
        for z in self._x:
            if isinstance(self.constant,dict):
                self.fillna[z] = self.constant[z]
            else:
                self.fillna[z] = self.constant
        self._fitted = True

class ReplaceMissingCategorical(BaseMissingTransformer):
    
    def __init__(self, constant: Union[str,dict] = "_MISSING_"):
        super(ReplaceMissingCategorical, self).__init__()
        self.constant = constant
        
    def fit(self, df, x: Union[str,list]):
        if self._fitted: return
        if isinstance(x,str): x = [x]
        self._x = x
        for z in self._x:
            if isinstance(self.constant, dict):
                self.fillna[z] = self.constant[z]
            else:
                self.fillna[z] = self.constant
        self._fitted = True