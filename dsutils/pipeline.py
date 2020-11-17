import pandas as pd
import numpy as np

class Pipeline:
    
    def __init__(self,steps):
        self._steps = steps
        self._validate_steps(steps)
        
    def _validate_steps(self, steps):
        for step in steps:
            self._validate_step(step)
            
    def _validate_step(self, step):
        if not isinstance(step[0],str):
            msg = "First component of a step must " + \
                  "be the name of the step"
            raise ValueError(msg)
        if not all(hasattr(step[1],attr) for attr in
                  ['fit','transform','fit_transform']):
            msg = "Step does not have at least one of " + \
                  "'fit', 'transform' or " + \
                  "'fit_transform' methods"
            raise ValueError(msg)
        if not type(step[2]) in [str,list]:
            msg = "Step needs to have column names to use"
            raise ValueError(msg)
            
    def fit(self, df):
        step_input = df
        for step in self._steps:
            self._fit_step(step, step_input)
            step_input = self._transform_step(step,step_input)
            
    def _fit_step(self,step,step_input):
        step[1].fit(step_input,step[2])
        
    def _transform_step(self,step,step_input):
        return(step[1].transform(step_input))
    
    def transform(self, df):
        step_input = df
        for step in self._steps:
            step_input = self._transform_step(step, step_input)
        return(step_input)
    
    def fit_transform(self, df):
        self.fit(df)
        return(self.transform(df))