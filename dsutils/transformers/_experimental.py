import pandas as pd
import numpy as np
from typing import Union
from sklearn.preprocessing import OneHotEncoder
from scipy import sparse

class OneHotComboSparse:
    def __init__(self,cols_to_enc,num_cols):
        if isinstance(cols_to_enc,str): [cols_to_enc] 
        self.cols_to_enc = cols_to_enc
        self.num_cols = num_cols
        self._fitted = False

    def fit(self, df):
        self.enc = OneHotEncoder(handle_unknown='ignore')
        
        self.enc.fit(df[self.cols_to_enc])
        self.all_preds = enc.get_feature_names(
            self.cols_to_enc).tolist() + self.num_cols
        self._fitted = True

    def transform(self, df):
        cat_encoded = self.enc.transform(df[self.cols_to_enc])
        num_to_sparse = sparse.csr_matrix(df[self.num_cols].values)
        X = sparse.hstack([cat_encoded,num_to_sparse])
        return(X)

    def fit_transform(self, df):
        self.fit(df)
        X = self.transform(df)
        return(X)
