import scipy.stats as ss
import numpy as np

def cramers_corrected_stat(confusion_matrix):
    """
    Calculate Cramers V statistic for categorial-categorial association.
    Uses correction from Bergsma and Wicher, 
    Journal of the Korean Statistical Society 42 (2013): 323-328
    
    See:
    https://stackoverflow.com/questions/20892799/
    using-pandas-calculate-cram%C3%A9rs-coefficient-matrix
    """
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))    
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return(np.sqrt(phi2corr / min( (kcorr-1), (rcorr-1))))