import pytest
import pandas as pd
from dsutils.utils.histograms import numeric_histogram

@pytest.fixture
def example_data():
    return(
        pd.DataFrame(
           {'x':[
               0, 1, 2.2, 1, 3.1,
               -0.23, 1, 2.3, 0, -0.5,
               2, 1.1 ]}
    ))

@pytest.mark.mpl_image_compare
def test_numeric_histogram(example_data):
    nh = numeric_histogram(
      example_data,
      x = 'x',
      line_columns = None,
      max_levels = 5,
      stat = 'mean',
      min_levels = 5,
      normalize = True)
    return nh