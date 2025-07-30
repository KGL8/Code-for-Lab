# params.py
import numpy
from numpy import sqrt, sin, cos, array, arctan, linspace, searchsorted
from helpers import build_sampler
from functools import lru_cache, wraps

# I am setting c=1 in all formulas

# Physical constants
# p = 0           # momentum of the photon (MeV/c) Uninitialized until γE is sampled
mp = 938.28     # mass of the proton (MeV/c^2)
mn = 939.57     # mass of the neutron (MeV/c^2)
md = 1875.61    # mass of the deuteron (MeV/c^2)

# Computed values
# v = p / (p + md)        # velocity of the CM frame
# γ = 1 / sqrt(1 - v**2)  # Lorentz factor

a0 = 0.0000000001       # almost zero

# Misc
γErange = (3,20)  # For simulation: we are only interested in firing off photons with γE in γErange.

# Derived momentum for neutron and proton in CM frame
# EγCM = γ * p * (1 - v)
# a = EγCM + sqrt(md**2)
# pn = sqrt(((a**2 + mn**2 - mp**2)**2 - 4 * a**2 * mn**2) / (4 * a**2))

# Physical Functions
# @precached_sampler(grid_size=500)
# def nθCM_PDF(x):
#     return 3/(x*x+1)

# Scene constants
O_T_dist = 10    # distance origin->target along z
T_width = 0.3    # target width along x
T_height = 2.5   # target height along y
T_depth = 3.8    # target depth along z
D_width = 5      # detector width along x
D_height = 20    # detector height along y
D_depth = 10     # detector depth along z
α1 = numpy.pi*1/2
α2 = numpy.pi*3/4
α3 = numpy.pi*31/36
α4 = numpy.pi*1/4
T_min = array([-T_width / 2, -T_height / 2, O_T_dist])                  # maximum point on target
T_max = array([T_width / 2, T_height / 2, T_depth + O_T_dist])          # minimum point on target
θ_max = arctan(sqrt((T_height / 2)**2 + (T_width / 2)**2) / O_T_dist)   # maximum theta value on target

# (a rad, r meters) 
D_pos = lambda a, r: array((-r*100*sin(a), 0, T_depth / 2 + O_T_dist - r*100*cos(a)))
D_minmax = lambda p: [p - array((D_width/2, D_height/2, D_depth/2)), p + array((D_width/2, D_height/2, D_depth/2))]
D_90_pos = D_pos(α1,20)
D_135_pos = D_pos(α2,20)
D_155_pos = D_pos(α3,12.8)
D_45_pos = D_pos(α4,20)
D_90_minmax = D_minmax(D_90_pos)
D_135_minmax = D_minmax(D_135_pos)
D_155_minmax = D_minmax(D_155_pos)
D_45_minmax = D_minmax(D_45_pos)

def γ_depth_PDF(x):
    return 1/(2*x+1)

def scaled_γ_depth_PDF(u, d):
    return d / (2 * u * d + 1)

depth_sampler = build_sampler(lambda u: scaled_γ_depth_PDF(u, 1), 0, 1, grid_size=500)

def sample_depth(max_depth):
    return depth_sampler().item() * max_depth


def γ_E_lvl_PDF(x):
    return 1/(x+0.1)

γ_E_lvl_PDF_sampler = build_sampler(γ_E_lvl_PDF, *γErange, grid_size=500)

# Below is the code to generate a range of PDFs with respect to photon energy. For e_grid_size values
# of γE, we generate the corresponding, single-valued γ_E_to_θ_PDF. Later (on photon spawn), when we
# know what γE to take, we select the correct precached PDF.

e_grid_size = 100
e_grid = linspace(*γErange, e_grid_size)

precached_samplers_with_e = []

def init_per_photon_sampling():
    for e_val in e_grid:
        def pdf(x, e=e_val):
            return 2 ** (-e * x)

        sampler = build_sampler(pdf, 0, θ_max, grid_size=500)
        precached_samplers_with_e.append(sampler)

def get_sampler(E_lvl):
    idx = searchsorted(e_grid, E_lvl)
    if idx == 0:
        return precached_samplers_with_e[0]
    elif idx == len(e_grid):
        return precached_samplers_with_e[-1]
    else:
        left = e_grid[idx - 1]
        right = e_grid[idx]
        best_idx = idx - 1 if abs(E_lvl - left) < abs(E_lvl - right) else idx
        return precached_samplers_with_e[best_idx]