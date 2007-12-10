##--------------------------------------------------------------------
## Exceptions
##--------------------------------------------------------------------
class GenericError(Exception):
    pass

class NotSquare(GenericError):
    pass

class NotVectorOrScalar(GenericError):
    def __str__(self):
        return "A scalar or vector is required"


def _assertVectorOrScalar(x):
    if x.shape[0] != 1 and x.shape[1] != 1:
        raise NotVectorOrScalar

