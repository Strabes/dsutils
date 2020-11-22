import numpy as np
import pandas as pd
from typing import Union

class BaseTransformer:
    """
    Base class for all transformers
    """
    
    def __init__(self,x: Union[str,list]):
        if isinstance(x,str): x = [x]
        self._x = x
        self._fitted = False
        
    def _reset(self):
        self._fitted = False
        
    def _check_if_fit(self):
        return(self._fitted)
    
    def _validate_x(self, df, x, dtypes):
        if len(x) == 1:
            self._validate_one(df, x, dtypes)
        else:
            for z in x:
                self._validate_one(df, z, dtypes)
                
    def fit_transform(self, df, in_place = False):
        self.fit(df)
        if in_place:
            self.transform(df, in_place)
        else:
            return(self.transform(df, in_place))
        
    def _validate_one(self, df, x, dtypes):
        if not x in df.columns:
            raise ValueError(x + " is not a column in the DataFrame")
        else:
            self._validate_one_dtype(df, x, dtypes)

            
    def _validate_one_dtype(self, df, x, dtypes):
        if not df[x].dtypes in dtypes:
            dtypes_str = ", ".join([str(t) for t in dtypes])
            raise TypeError(
                x + " is not one of the excepted dtypes: " + dtypes_str)
        else:
            pass