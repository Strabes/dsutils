from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class VectorizeText(BaseEstimator, TransformerMixin):

    def __init__(self, vectorizer = TfidfVectorizer(), params : dict = None):
        self.vectorizer = vectorizer

    def fit(self, X, y = None):
        self.vectorizer = self.vectorizer.fit(X, y)
        return self
    
    def transform(self, X):
        res = self.vectorizer.transform(X)
        ref_df = pd.DataFrame(
            res.todense(),
            
        )