import pytest
import pandas as pd
import numpy as np
from distutils import dir_util

from dsutils.utils.binners import *

def test_cutpoints():
    x = np.array([1.213,43,9.32,4.22324,-1.6,5.2321,32,0.123])
    z = np.array([-1.6, -1.3, 19.9, 41.1, 43. ])
    y = cutpoints(x,ncuts=3,sig_fig=3)
    assert np.array_equal(z,y)

def test_human_readable_num():
    assert human_readable_num(20.321) == '20.3'
    assert human_readable_num(20321) == '20.3K'


@pytest.fixture
def example_data():
    return(
        pd.DataFrame(
           {'x':[
               0, 1, 2.2, 1, 3.1,
               -0.23, 1, 2.3, 0, -0.5,
               2, 1.1 ]}
    ))

def test_cutter(datadir,example_data):
    c = pd.Categorical(
        ['02: 0', '04: 1', '05: (1, 2.98]',
        '04: 1', '06: (2.98, 3.1]', '01: [-0.5, 0)',
        '04: 1', '05: (1, 2.98]', '02: 0',
        '01: [-0.5, 0)', '05: (1, 2.98]',
        '05: (1, 2.98]'],
        categories = [
            '01: [-0.5, 0)', '02: 0', '03: (0, 1)',
            '04: 1', '05: (1, 2.98]','06: (2.98, 3.1]'])
    x = pd.Series(cutter(example_data,'x',3))
    assert x.equals(pd.Series(c))