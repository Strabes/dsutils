import pytest
import pandas as pd
import numpy as np
#from distutils import dir_util
import math

from dsutils.monitoring.psi import PSI

def test_PSI():
    df1 = pd.DataFrame({
        'x' : ['a']*6 + ['b']*5,
        'y' : ['a']*3 + ['b']*2 + list('cdefgh')})
    df2 = pd.DataFrame({
        'x' : ['a']*5 + ['b']*4,
        'y' : ['a']*3 + ['b']*2 + list('cefj')})
    psi = PSI()
    psi.fit(df1)
    res = psi.transform(df2)
    res = {k:round(v,5) for k,v in res.items()}
    assert res == {'x': 0.00041, 'y': 4.4372}