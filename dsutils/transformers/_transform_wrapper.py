"""
TransformWrapper is a generic class for wrapping
functions that do not have parameter that need to
be learned from the data. This class implements
fit, transform and fit_transform methods for the function.
"""

from ._base import BaseTransformer


class TransformWrapper(BaseTransformer):
    """
    Generic class for wrapping functions that
    do not have parameters that need to be learned
    from the data. This class implements fit, transform
    and fit_transform methods for the function.
    """
    def __init__(self, func, **kwargs):
        """
        Parameters
        ----------

        func : callable
            A function with a single argument, a pandas.DataFrame,
            and which returns a pandas.DataFrame
        """
        self._func = func
        self._kwargs = kwargs
        self._fitted = False

    def fit(self, df):
        """Fit method
        Parameters
        ----------
        df : pandas.DataFrame
        """
        self._fitted = True

    def transform(self, df, in_place=False):
        """Transform method
        Parameters
        ----------
        df : pandas.DataFrame

        in_place : Boolean
          default : False
        """
        if not self._fitted:
            raise Exception("Transformation not fit yet")
        if not in_place:
            df = df.copy()
        df = self._func(df, **self._kwargs)
        if not in_place:
            return(df)
