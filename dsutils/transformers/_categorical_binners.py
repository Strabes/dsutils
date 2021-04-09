import pandas as pd
import numpy as np
from typing import Union, Optional
from ._base import BaseTransformer

class _CategoricalBinner(BaseTransformer):
    """
    Base class for all categorical binnning transformers
    """
    def __init__(self, variables = Union[str,list]):
        super(_CategoricalBinner, self).__init__(variables)
        self.map = {}
        self.other_val = None
        
    def transform(self, X : pd.DataFrame):
        """
        Default transform method
        
        Parameters
        ----------
        X : pandas.DataFrame
        
        Returns
        -------
        pandas.DataFrame
        """
        if not self.fitted:
            raise Exception("Transformation not fit yet")

        X = X.copy()

        for z in self.variables:
            X.loc[-X[z].isna(),z] = X.loc[-X[z].isna(),z] \
                .map(self.map[z]).fillna(self.other_val)
        
        return(X)

        
class MaxLevelBinner(_CategoricalBinner):
    """
    MaxLevelBinner
    """
    def __init__(self, variables: Union[str,list], max_levels = 20, other_val = '_OTHER_'):
        super(MaxLevelBinner, self).__init__(variables)
        self.max_levels = max_levels
        self.other_val = other_val
        
    def fit(self, X, y : Optional[pd.Series] = None):
        """
        Fit method
        
        Parameters
        ----------
        X : pandas.DataFrame
        """
        if self.fitted: return
        for z in self.variables:
            cnts = X.groupby(z,dropna=False).size() \
                     .sort_values(ascending = False) \
                     .head(self.max_levels)
            levels = cnts.index.tolist()
            self.map[z] = {l:l for l in levels}
        self.fitted = True

        
class PercentThresholdBinner(_CategoricalBinner):
    """
    PercentThresholdBinner
    """
    def __init__(self, variables: Union[str,list], percent_threshold = 0.02, other_val = '_OTHER_'):
        super(PercentThresholdBinner, self).__init__(variables)
        self.percent_threshold = percent_threshold
        self.other_val = other_val
        
    def fit(self, X, y : Optional[pd.Series] = None):
        """
        Fit method
        
        Parameters
        ----------
        df : pandas.DataFrame
        """
        if self.fitted: return
        for z in self.variables:
            cnts = (X.groupby(z,dropna=False).size() / X.shape[0])
            levels = cnts[cnts>=self.percent_threshold].index.tolist()
            self.map[z] = {l:l for l in levels}
        self.fitted = True
        
        
class CumulativePercentThresholdBinner(_CategoricalBinner):
    """
    CumulativePercentThresholdBinner
    """
    def __init__(self, variables: Union[str,list], cum_percent = 0.95, other_val = '_OTHER_'):
        super(CumulativePercentThresholdBinner, self).__init__(variables)
        self.cum_percent = cum_percent
        self.other_val = other_val
        
    def fit(self, X, y=None):
        """
        Fit method
        
        Parameters
        ----------
        X : pandas.DataFrame
        """
        if self.fitted: return
        for z in self.variables:
            cnts = (X.groupby(z,dropna=False).size() / X.shape[0]) \
                      .to_frame(name = z + '_perc').reset_index() \
                      .sort_values([z + '_perc',z], ascending = [False,True]) \
                      .set_index(z) \
                      .cumsum().shift(periods=1, fill_value=0)
            levels = cnts[cnts[z + '_perc']<=0.85].index.tolist()
            self.map[z] = {l:l for l in levels}
        self.fitted = True