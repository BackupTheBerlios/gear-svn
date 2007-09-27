from numpy import *



x = mat(random.rand(3,2))
y = mat(random.rand(3,2))
z = mat(random.rand(3,1))

h  = array( [ (1.5,2,3), (4,5,6) ,(10,20,30)] )




numpy.concatenate((numpy.repeat(numpy.asmatrix(1), 40), x))


def cbind(x,y):
    z = concatenate((x,y),1)
    return(z)


def rbind(x,y):
    z = concatenate((as.matrix(x),as.matrix(y)),0)
    return(z)


