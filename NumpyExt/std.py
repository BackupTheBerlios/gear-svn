###-------------------------------------------------------------------
###  std.py - GEAR standard library
###
###        code (C) 2007-2007 Christine Choirat
###
###  Email: cchoirat@orange.fr
###
###  This file:
###    created 2007-07-29
###    last modified 2007-08-02
###-------------------------------------------------------------------

import scipy as S
import scipy.linalg

##--------------------------------------------------------------------
## Matrix class
##--------------------------------------------------------------------

class mat(S.matrix):
    """Matrix class allowing easy concatenation.
    
    A not-so-nice hack with operator overloading allows for using:
      | for row stack
      & for column stack
    """
    def cbind(self, other):
        try:
            res = S.concatenate((self, other), 1)
            return res
        except ValueError:
            if self.shape == (1, 1):
                iLen = other.shape[0]
                m  = self[0, 0] * S.ones((iLen, 1))
                res = S.concatenate((m, other), 1)
                return res
            elif other.shape == (1, 1):
                iLen = self.shape[0]
                m  = other[0, 0] * S.ones((iLen, 1))
                res = S.concatenate((self, m), 1)
                return res
            else:
                print 'matrix dimensions do not match'
                raise
        except:
            print 'Unexpected error:', sys.exc_info()[0]
            raise
    def rbind(self, other):
        try:
            res = S.concatenate((self, other), 0)
            return res
        except ValueError:
            if self.shape == (1, 1):
                iLen = other.shape[1]
                m  = self[0, 0] * S.ones((1, iLen))
                res = S.concatenate((m, other), 0)
                return res
            elif other.shape == (1, 1):
                iLen = self.shape[1]
                m  = other[0, 0] * S.ones((1, iLen))
                res = S.concatenate((self, m), 0)
                return res
            else:
                print 'matrix dimensions do not match'
                raise
        except:
            print 'Unexpected error:', sys.exc_info()[0]
            raise
    def __or__(self, other):
        return self.rbind(other)
    def __and__(self, other):
        return self.cbind(other)

## ## Test sample:
B = mat((1, 2, 3))
b = B.T
A = mat(S.floor(10 * S.random.random((2, 3))))
a = A.T
## print A.T | B.T
## print
## print A & B
## print
## print mat(1) | B
## print
## print A & mat(1)

##--------------------------------------------------------------------
## Matrix creation
##--------------------------------------------------------------------

def constant(dval, r=None, c=None):
    """Matrix filled with dval.

    If r and c are numbers, it returns a (r, c) matrix,
    r and c being converted to integers when needed.

    If r is a (m, n) matrix, it returns an (m, n) matrix.   
    """
    return dval * ones(r, c)

def diag(ma):
    """Diagonal matrix with ma on the diagonal.

    ma needs to be (1, k) or (k, 1).
    """
    ma = mat(ma)
    if ma.shape[0] == 1 or ma.shape[1] == 1:
        return S.diagflat(ma)
    else:
        print 'matrix dimensions do not match'
 
def range(min, max, step=None):
    """ Values between min and max by step.

    If no value is provided, step is set to 1.
    """
    if step is None:
        return mat(S.arange(min, max + 1))
    else:
        return mat(S.arange(min, max + step, step))

def ones(r, c=None):
    """Matrix filled with dval.

    If r and c are numbers, it returns a (r, c) matrix,
    r and c being converted to integers when needed.

    If r is a (m, n) matrix, it returns an (m, n) matrix.   
    """
    try:
        return mat(S.ones((r, c)))
    except TypeError:
        return mat(S.ones(r.shape))

def toeplitz(ma, cm=None):
    """
    Symmetric Toeplitz matrix.

    ma is a (k, 1) or (1, k) matrix.

    The Toeplitz matrix is of dimension (cm, cm)
    if cm is provided. Otherwise, it is (k, k)
    """
    ma = mat(ma)
    if ma.shape[0] != 1 and ma.shape[1] != 1:
        return 'matrix dimensions do not match'
    elif type(cm) == None:
        return S.linalg.basic.toeplitz(ma)
    else:
        m = ma.flatten()
        if cm is None:
            return S.linalg.basic.toeplitz(ma)
        else:
            if cm >= m.shape[1]: 
                n = m & zeros(mat(1), cm -  m.shape[1])
                return S.linalg.basic.toeplitz(n)
            else:
                return S.linalg.basic.toeplitz(m[0:cm, 0:cm])

def unit(r, c=None):
    """Identity matrix.

     If r and c are numbers, it returns a (r, c) matrix,
    r and c being converted to integers when needed.

    If r is a (m, n) matrix, it returns an (m, n) matrix. 
    
    """
    try:
        return mat(S.eye(r, c))
    except TypeError:
        return mat(S.eye(r.shape[0], r.shape[1]))

def zeros(r, c=None):
    """Matrix filled with zeros.

    If r and c are numbers, it returns a (r, c) matrix,
    r and c being converted to integers when needed.

    If r is a (m, n) matrix, it returns an (m, n) matrix.   
    """
    try:
        return mat(S.zeros((r, c)))
    except TypeError:
        return mat(S.zeros(r.shape))

##--------------------------------------------------------------------
## Random numbers
##--------------------------------------------------------------------
   
def ranu(r, c):
    """(r, c) matrix (filled by row) of uniform random numbers.

    r and c are converted to integers when needed.
    """
    return mat(S.random.rand(r, c))

def rann(r, c):
    """(r, c) matrix (filled by row) of standard normal random numbers.

    r and c are converted to integers when needed.
    
    """
    return mat(S.random.rand(r, c))

## def ranseed(iseed):

###-------------------------------------------------------------------
### TO DO:
###   o handle errors and exceptions better
###   x use shorcuts when importing numpy and scipy
###   o write doctest and examples
###   x avoid numpy when possible. use scipy instead
###   o doc for range and toeplitz
###-------------------------------------------------------------------

def spam():
    """Do nothing, but document it.
    
    No, really, it doesn't do anything.
    """
    pass


def naiveols(mx, my):
    """Naive ols implementation.

    Does very little and not even very well!
    """
    mb = (mx.T * mx).I * mx.T * my
    return mb

## There is a lot to do...
