import pytest
import pandas as pd
import numpy as np

from ..transformers._categorical_binners import *

@pytest.fixture
def example_data():
    return(pd.DataFrame(
    {'x':['a','a','b','c','b','a','a'],
     'y':['a','b','c','d','e','a','b']}
    ))


@pytest.fixture
def example_data_na():
    return(pd.DataFrame(
    {'x':['a','a','b','c','b','a',np.nan,'a',np.nan]}
    ))

def test_max_level_binner(example_data):
    response = pd.DataFrame({
        'x':['a','a','b','_OTHER_','b','a','a'],
        'y':['a','b','_OTHER_','_OTHER_','_OTHER_','a','b']
    })
    mlb = MaxLevelBinner(x = ['x','y'], max_levels = 2, other_val = '_OTHER_')
    ft = mlb.fit_transform(example_data)
    assert ft.equals(response)