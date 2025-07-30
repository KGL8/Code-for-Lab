# imports.py
import numpy
import matplotlib.pyplot as plt
from numpy import array, asarray, float64, float32, uint32, sin, cos, arccos, sqrt, cross, dot, arctan, tan, mod, pi, append, eye, allclose, sum, put, linspace, interp, trapezoid
from scipy.integrate import cumulative_trapezoid, quad
from numpy.linalg import norm, inv
from random import random as rnd, uniform as uni
from dataclasses import dataclass, field
from params import *
from helpers import ray_through_aabb, sph_car, rotate_point_to_vector, vector_to_list, norm3
from functools import lru_cache, wraps

globals().update({name: globals()[name] for name in dir() if not name.startswith('__')})

def vec(a,b,c):
    return array([a,b,c])

def vec2(a,b):
    return array([a,b])