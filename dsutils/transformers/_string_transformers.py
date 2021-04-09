import numpy as np
import pandas as pd
from typing import Union
import re

from ._base import BaseTransformer

class RegexReplacer(BaseTransformer):
    """
    Replace Regex Expressions
    """
    def __init__(self, variables : Union[str,list], pattern : str,
                 replacement = '', case_sensitive = False, strip = True,
                 replacement_type = 'pattern'):
        """
        Regex Replacer
        
        Parameters
        ----------
        variables : str or list
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
        super(RegexReplacer, self).__init__(variables)
        self.pattern = pattern
        self.replacement = replacement
        self.case_sensitive = case_sensitive
        self.strip = strip
        self.replacement_type = replacement_type
        
    def fit(self, X, y = None):
        self.fitted = True
        
    def transform(self, X):
        """
        Transform method
        """
        if not self.fitted:
            raise Exception("Transformation not fit yet")
        X = X.copy()
        for z in self.variables:
            X.loc[:,z] = X[z].map(self.replacer)
        return X
        
    def _replacer(self,x):
        if self.replacement_type == 'pattern':
            if self.case_sensitive:
                s = re.sub(self.pattern,self.replacement,x)
            else:
                s = re.sub(self.pattern,self.replacement,x,flags=re.I)
        elif self.replacement_type == 'all':
            if self.case_sensitive:
                s = re.search(self.pattern,self.replacement,x)
            else:
                s = re.search(self.pattern,x,flags=re.I)
            s = x if not s else self.replacement
            return(s)
        return(s)
    

class StringFormatter(BaseTransformer):
    
    def __init__(self):
        pass