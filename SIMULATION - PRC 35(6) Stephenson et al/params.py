# params.py
from numpy import sqrt, array, arctan, pi

# Physical constants
p = 800         # momentum of the photon (MeV/c)
mp = 938.28     # mass of the proton (MeV/c^2)
mn = 939.57     # mass of the neutron (MeV/c^2)
md = 1875.61    # mass of the deuteron (MeV/c^2)

# Computed values
v = p / (p + md)   # Velocity of the CM frame
γ = 1 / sqrt(1 - v**2)  # Lorentz factor

# Derived momentum for neutron and proton in CM frame
EγCM = γ * p * (1 - v)
a = EγCM + sqrt(md**2)
pn = sqrt(((a**2 + mn**2 - mp**2)**2 - 4 * a**2 * mn**2) / (4 * a**2))

# Scene constants
O_T_dist = 10    # distance origin->target along z
T_width = 0.3    # target width along x
T_height = 2.5   # target height along y
T_depth = 3.8    # target depth along z
D_width = 5      # detector width along x
D_height = 20    # detector height along y
D_depth = 10     # detector depth along z
α1 = pi*1/2
α2 = pi*3/4
α3 = pi*31/36
T_min = array([-T_width / 2, -T_height / 2, O_T_dist])
T_max = array([T_width / 2, T_height / 2, T_depth + O_T_dist])
θ_max = arctan(sqrt((T_height / 2)**2 + (T_width / 2)**2) / O_T_dist)