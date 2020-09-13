import pandas as pd

def _groupby_apply_ungroup(func,df,groupby):
    _df = df.copy()
    _df.groupby(groupby).transform(func)
    return(_df)