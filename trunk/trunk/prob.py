
import numpy as N
import numpy.random as R
import scipy as S
import scipy.linalg as L
from numpy import ndarray
from numpy.core.defmatrix import matrix, asmatrix
from exceptions import *



##--------------------------------------------------------------------
## Random numbers
##--------------------------------------------------------------------
   
def ranu(r, c):
    """(r, c) matrix (filled by row) of uniform random numbers.

    r and c are converted to integers when needed.
    """
    return N.mat(R.rand(r, c))

def rann(r, c):
    """(r, c) matrix (filled by row) of standard normal random numbers.

    r and c are converted to integers when needed.
    
    """
    return N.mat(R.randn(r, c))
