###-------------------------------------------------------------------
###  std.py - GEAR standard library
###
###        code (C) 2007-2007 Christine Choirat
###
###  Email: cchoirat@gmail.com
###         paolo.tenconi@gmail.com
###
###  This file:
###    created 2007-07-29
###    last modified 2007-09-25
###-------------------------------------------------------------------

import numpy as N
import numpy.random as R
import scipy as S
import scipy.linalg as L
from numpy import ndarray
from numpy.core.defmatrix import matrix, asmatrix

from exceptions import *






##--------------------------------------------------------------------
## Matrix utilities
##--------------------------------------------------------------------

        
def pmat(m, rownames=None, colnames=None):
    """
    Prints a matrix with row and column names.
    Slightly modified version of Andrew Straw's function taken from file
    'DataFrame.py'.
    Copyright (c) 2001-2006, Andrew Straw.
    (See http://www.its.caltech.edu/~astraw/.)
    """
    r, c = m.shape
    if rownames is None:
        rownames = ['R' + str(i) for i in xrange(r)]
    if colnames is None:
        colnames = ['C' + str(i) for i in xrange(c)]
    def cc(s, width=10, just='center'):
        if len(s) > width:
            s = s[:width]
        if just=='center':
            return s.center(width)
        elif just=='left':
            return s.ljust(width)
        elif just=='right':
            return s.rjust(width)
    print cc('', width=5, just='right'),
    for field in colnames:
        print cc(field, width=5, just='right'),
    print ''
    for i in xrange(r):
        print cc(rownames[i], width=5, just='right'),
        for j in xrange(c):
            print cc(str(m[i, j]), width=5, just='right'),
        print ''
    




##--------------------------------------------------------------------
## Matrix creation
##--------------------------------------------------------------------

def zeros(r, c=None,dtype=None):
    """Matrix filled with zeros.

    If r and c are numbers, it returns a (r, c) matrix,
    r and c being converted to integers when needed.

    If r is a (m, n) matrix, it returns an (m, n) matrix.   
    """
    try:
        a = ndarray.__new__(matrix,(r,c),dtype)
    except TypeError:
        a = ndarray.__new__(matrix,r.shape,dtype)
    a.fill(0)
    return(a)
	
def ones(r, c=None,dtype=None):
    """Matrix filled with ones.

    If r and c are numbers, it returns a (r, c) matrix,
    r and c being converted to integers when needed.

    If r is a (m, n) matrix, it returns an (m, n) matrix.   
    """
    try:
        a = ndarray.__new__(matrix,(r,c),dtype)
    except TypeError:
        a = ndarray.__new__(matrix,r.shape,dtype)
    a.fill(1)
    return(a)

def constant(dval,r, c=None,dtype=None):
    """Matrix filled with dval.

    If r and c are numbers, it returns a (r, c) matrix,
    r and c being converted to integers when needed.

    If r is a (m, n) matrix, it returns an (m, n) matrix.   
    """  
    try:
        a = ndarray.__new__(matrix,(r,c),dtype)
    except TypeError:
        a = ndarray.__new__(matrix,r.shape,dtype)
    a.fill(dval)
    return(a)

def unit(r, c=None,dtype=None):
    """Identity matrix.

     If r and c are numbers, it returns a (r, c) matrix,
    r and c being converted to integers when needed.

    If r is a (m, n) matrix, it returns an (m, n) matrix. 
    
    """
    try:
        return asmatrix(N.eye(r, c, dtype=dtype))
    except TypeError:
        return asmatrix(N.eye(r.shape[0], r.shape[1], dtype=dtype))

def diag(ma):
    """Diagonal matrix with ma on the diagonal.

    ma needs to be (1, k) or (k, 1).
    """
    _assertVectorOrScalar(asmatrix(ma))
    ma = N.mat(ma)
    return S.diagflat(ma)
 
def range(min, max, step=None):
    """ Values between min and max by step.

    If no value is provided, step is set to 1.
    """
    if step is None:
        return asmatrix(S.arange(min, max + 1))
    else:
        return asmatrix(S.arange(min, max + step, step))


def toeplitz(ma, cm=None):
    """
    Symmetric Toeplitz matrix.

    ma is a (k, 1) or (1, k) matrix.

    The Toeplitz matrix is of dimension (cm, cm)
    if cm is provided. Otherwise, it is (k, k)
    """
    ma = asmatrix(ma)
    _assertVectorOrScalar(ma)
    if type(cm) == None:
        return asmatrix(L.basic.toeplitz(ma))
    else:
        m = ma.flatten()
        if cm is None:
            return asmatrix(L.basic.toeplitz(ma))
        else:
            if cm >= m.shape[1]: 
                n = cbind(zeros(N.mat(1), cm -  m.shape[1]))
                return asmatrix(L.basic.toeplitz(n))
            else:
                return asmatrix(L.basic.toeplitz(m[0:cm, 0:cm]))
            


    
    
##--------------------------------------------------------------------
## Useful 
##--------------------------------------------------------------------

def cbind(source, *args):
    """Like the R cbind function.  It concatenates arrays column-wise
    and returns the result.  CAUTION:  If one array is shorter, it will be
    repeated until it is as long as the other.

    Format:  cbind (source, args)    where args=any # of arrays
    Returns: an array as long as the LONGEST array past, source appearing on the
    'left', arrays in <args> attached on the 'right'.\n

    Remark: adapted from scipy.stats._support (function 'abut')"""

    source = N.asarray(source)
    if len(source.shape)==1:
        width = 1
        source = N.resize(source,[source.shape[0],width])
    else:
        width = source.shape[1]
    for addon in args:
        if len(addon.shape)==1:
            width = 1
            addon = N.resize(addon,[source.shape[0],width])
        else:
            width = source.shape[1]
        if len(addon) < len(source):
            addon = N.resize(addon,[source.shape[0],addon.shape[1]])
        elif len(source) < len(addon):
            source = N.resize(source,[addon.shape[0],source.shape[1]])
        source = N.concatenate((source,addon),1)
    return source

def rbind(source, *args):
    """Like the R rbind function.  It concatenates arrays row-wise
    and returns the result.  CAUTION:  If one array is shorter, it will be
    repeated until it is as long as the other.

    Format:  rbind (source, args)    where args=any # of arrays
    Returns: an array as long as the LONGEST array past, source appearing on the
    'left', arrays in <args> attached on the 'right'.\n

    Remark: adapted from scipy.stats._support (function 'abut')"""

    source = N.asarray(source)
    if len(source.shape)==1:
        height = 1
        source = N.resize(source,[height,source.shape[1]])
    else:
        height = source.shape[0]
    for addon in args:
        if len(addon.shape)==1:
            height = 1
            addon = N.resize(addon,[height, source.shape[1]])
        else:
            height = source.shape[0]
        if len(addon) < len(source):
            addon = N.resize(addon,[addon.shape[0], source.shape[1]])
        elif len(source) < len(addon):
            source = N.resize(source,[source.shape[0], addon.shape[1]])
        source = N.concatenate((source,addon),0)
    return source

    



##--------------------------------------------------------------------
## MAIN
##--------------------------------------------------------------------

if __name__ == "__main__":
    a = zeros(4,2)
    print(a)

    b = (2,3,4)
    b = zeros(3,2)
    
    diag(b)
    
    
	
	
