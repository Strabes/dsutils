import numpy as np
import pandas as pd
from typing import Union
import re

from ._base import BaseTransformer

class RegexReplacer(BaseTransformer):
    """
    Replace Regex Expressions
    """
    def __init__(self, x : Union[str,list], pattern : str,
                 replacement = '', case_sensitive = False, strip = True,
                 replacement_type = 'pattern'):
        """
        Regex Replacer
        
        Parameters
        ----------
        x : str or list
            Variable(s) to transform
        
        pattern : str
            Regex to replace
        
        replacement : str
            String to replace 'pattern' with
        
        case_sensitive : boolean
            If True, regex match is not case sensitive
        
        strip : boolean
            If True, strip whitespace from x variables
            
        replacement_type : str
            'pattern' - replace just the matched pattern
            'all' - replace the entire string when match is found
        """
        super(RegexReplacer, self).__init__(x)
        self._pattern = regex
        self._replacement = replacement
        self._case_sensitive = case_sensitive
        self._strip = strip
        self._replacement_type = replacement_type
        
    def fit(self, df):
        self._fitted = True
        
    def transform(self, df, in_place = False):
        """
        Transform method
        """
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        for z in self._x:
            df.loc[:,z] = df[z].map(self._replacer)
        if not in_place: return(df)
        
    def _replacer(self,x):
        if self._replacement_type == 'pattern':
            if self._case_sensitive:
                s = re.sub(self._pattern,self._replacement,x)
            else:
                s = re.sub(self._pattern,self._replacement,x,flags=re.I)
        elif self._replacement_type == 'all':
            if self._case_sensitive:
                s = re.search(self._pattern,self._replacement,x)
            else:
                s = re.search(self._pattern,x,flags=re.I)
            s = x if not s else self._replacement
            return(s)
        return(s)
    

class StringFormatter(BaseTransformer):
    
    def __init__(self):
        pass