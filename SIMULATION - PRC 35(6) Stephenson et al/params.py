# params.py
from dataclasses import dataclass
from imports import *

@dataclass
class Constants:
    # distance origin->target
    O_T_dist: float = 10    # along z
    # target dimensions
    T_width: float = 0.3    # along x
    T_height: float = 2.5   # along y
    T_depth: float = 3.8    # along z
    # detctor dimensions
    D_width: float = 5      # along x
    D_height: float = 20    # along y
    D_depth: float = 10     # along z
    # particle parameters
    p: float = 800          # momentum of the photon
    mp: float = 938.28      # mass of the proton
    mn: float = 939.57      # mass of the neutron
    md: float = 1875.61     # mass of the deuteron
    # derivative parameters
    v = p/(p+md)            # velocity of the CM frame
    γ = 1/sqrt(1-v**2)      # Lorentz factor