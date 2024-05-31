import numpy as np
import random
from opensimplex.internals import _noise3, _init
from numba import njit


perm, perm_grad_index3 = _init(seed=16)


@njit(cache=True)
def Interpolate(tl, br):
    return (1 - tl) / (br - tl)

@njit
def noise3(x, y, z):
    return _noise3(x, y, z, perm, perm_grad_index3)

@njit
def get_triangles(time, loc, ):
