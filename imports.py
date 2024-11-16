# imports.py
import numpy
from numpy import array, float32, uint32, sin, cos, arccos, sqrt, cross, dot, arctan, tan, mod, pi, append, eye, allclose
from scipy.integrate import quad
from numpy.linalg import norm, inv
from random import random as rnd, uniform as uni
from dataclasses import dataclass, field
from params import *
from helpers import ray_through_aabb, sample_from_pdf, sph_car, rotate_point_to_vector
from functools import lru_cache

globals().update({name: globals()[name] for name in dir() if not name.startswith('__')})

def vec(a,b,c):
    return array([a,b,c])