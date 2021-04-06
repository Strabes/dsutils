import re
from typing import Union
import pandas as pd


def _col_selector(df, pattern = None, dtype_include : Union[str, list] = None,
    dtype_exclude = None, excl_pattern = None):
    """Select columns from pandas.DataFrame
    meeting certain requirements

    Parameters
    ----------
    df : pandas.DataFrame

    pattern : str
        regular expression to filter columns for

    dtype_include : Union[str, list]
        str or list of dtypes to include
    """
    cols = df.columns.tolist()
    d = df.dtypes.to_dict()
    if dtype_include is not None:
        cols = []
        if isinstance(dtype_include, str):
            dtype_include = [dtype_include]
        if 'object' in dtype_include:
            cols += [c for c,v in d.items() if v == 'object']
        if 'numeric' in dtype_include:
            cols += [c for c,v in d.items() if
                pd.api.types.is_numeric_dtype(v)]
    if dtype_exclude is not None:
        if isinstance(dtype_exclude, str):
            dtype_exclude = [dtype_exclude]
        if 'object' in dtype_exclude:
            # TODO: Figure out best way to drop
            pass
    if isinstance(pattern,str):
        cols = [c for c in cols if re.findall(pattern,c)]
    if isinstance(excl_pattern,str):
        cols = [c for c in cols if not re.findall(excl_pattern,c)]
    return cols


class ColumnSelector:
    """Class for selecting columns"""
    def __init__(self,**kwargs):
        self.kwargs = kwargs

    def __call__(self, df, *args):
        cols = _col_selector(df, **self.kwargs)
        return cols


class MakeTransformer:
    """Class for constructing a transformer once
    variables have been determined"""
    def __init__(self, transformer, **selectors):
        self.transformer = transformer
        self.selectors = selectors
        self._fitted = False

    def fit(self, df, *args):
        """fit wrapper method"""
        trans_args = {}
        for k,v in self.selectors.items():
            trans_args[k] = v(df)
        self.transformer = self.transformer(**trans_args)
        self.transformer.fit(df)
        self._fitted = True

    def transform(self, df):
        """transform wrapper method"""
        x = self.transformer.transform(df)
        return x

    def fit_transform(self, df, y = None):
        """fit_transform wrapper method"""
        self.fit(df)
        x = self.transform(df)
        return x
