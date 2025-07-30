# routines.py
from imports import *
from interface import * # type: ignore

# angle (rad) to differential cross section at various photon energies
MeV_to_cross_section_by_theta = {
3:   lambda x: 0.009476*sin(2*x-1.532)+0.01153,
3.5: lambda x: 0.01259*sin(2*x-1.521)+0.01406,
4:   lambda x: 0.01385*sin(2.001*x-1.512)+0.015,
4.5: lambda x: 0.01411*sin(2.001*x-1.504)+0.01506,
5:   lambda x: 0.01385*sin(2.001*x-1.498)+0.01466,
5.5: lambda x: 0.01333*sin(2.001*x-1.491)+0.01405,
6:   lambda x: 0.01269*sin(2.001*x-1.485)+0.01334,
6.5: lambda x: 0.01201*sin(2.001*x-1.479)+0.01262,
7:   lambda x: 0.01134*sin(2.001*x-1.474)+0.01191,
8:   lambda x: 0.01007*sin(2.001*x-1.464)+0.01059,
9:   lambda x: 0.008947*sin(2.001*x-1.454)+0.009441,
11:  lambda x: 0.007149*sin(2.001*x-1.436)+0.007621,
12:  lambda x: 0.006437*sin(2.001*x-1.427)+0.006906,
13:  lambda x: 0.005821*sin(2.001*x-1.419)+0.00629,
14:  lambda x: 0.005288*sin(2*x-1.41)+0.005758,
15:  lambda x: 0.004824*sin(2*x-1.401)+0.005297,
16:  lambda x: 0.004416*sin(2*x-1.392)+0.004892,
17:  lambda x: 0.004058*sin(1.999*x-1.384)+0.004536,
18:  lambda x: 0.003741*sin(1.998*x-1.375)+0.004222,
19:  lambda x: 0.003459*sin(1.997*x-1.366)+0.003942,
20:  lambda x: 0.003207*sin(1.996*x-1.357)+0.003693
}
# peaks of the above sinusoidal functions
MeV_to_x_sect_max_value = {
3:   0.009476 + 0.01153,
3.5: 0.01259 + 0.01406,
4:   0.01385 + 0.015,
4.5: 0.01411 + 0.01506,
5:   0.01385 + 0.01466,
5.5: 0.01333 + 0.01405,
6:   0.01269 + 0.01334,
6.5: 0.01201 + 0.01262,
7:   0.01134 + 0.01191,
8:   0.01007 + 0.01059,
9:   0.008947 + 0.009441,
11:  0.007149 + 0.007621,
12:  0.006437 + 0.006906,
13:  0.005821 + 0.00629,
14:  0.005288 + 0.005758,
15:  0.004824 + 0.005297,
16:  0.004416 + 0.004892,
17:  0.004058 + 0.004536,
18:  0.003741 + 0.004222,
19:  0.003459 + 0.003942,
20:  0.003207 + 0.003693
}
# angle (theta) to photon asymmetry at various photon energies
# Notes: This takes theta in degrees because the arenhovel data takes theta in degrees,
# and I literally just forgot to convert before performing the tedious task of fitting
# polynomials to the data. Fyi, despite the regression saying these all match with
# R^2 >= 0.995, there are sone pretty grossly unfitting functions in the teens,
# particularly those of degree 4. The world is messy, so if the R^2 is good enough
# then whatever.
MeV_to_photon_asymmetry_by_theta = {
3.0:  lambda x: 1.521183874e-12*x**6 - 8.113529748e-10*x**5 + 1.508797309e-07*x**4 - 1.085486832e-05*x**3 + 4.333373917e-05*x**2 + 0.02825288912*x - 0.01174708966,
3.5:  lambda x: -1.738446179e-08*x**4 + 6.272217735e-06*x**3 - 0.0008237682169*x**2 + 0.04636448864*x - 0.002132951945,
4.0:  lambda x: -1.334758305e-12*x**6 + 7.363500359e-10*x**5 - 1.734752668e-07*x**4 + 2.21240491e-05*x**3 - 0.00159328487*x**2 + 0.06087277177*x - 0.005972614104,
4.5:  lambda x: -2.10536374e-12*x**6 + 1.153453998e-09*x**5 - 2.598564961e-07*x**4 + 3.065914771e-05*x**3 - 0.001994656474*x**2 + 0.06810291596*x - 0.002651288538,
5.0:  lambda x: -2.594467253e-12*x**6 + 1.418196942e-09*x**5 - 3.145901469e-07*x**4 + 3.604274466e-05*x**3 - 0.002245527588*x**2 + 0.072536132*x - 0.0002549764926,
5.5:  lambda x: -2.895597583e-12*x**6 + 1.581285458e-09*x**5 - 3.482953665e-07*x**4 + 3.935156128e-05*x**3 - 0.002399002566*x**2 + 0.07521869468*x + 0.001320771375,
6.0:  lambda x: -3.068266254e-12*x**6 + 1.674986449e-09*x**5 - 3.676888881e-07*x**4 + 4.125591406e-05*x**3 - 0.002487119015*x**2 + 0.07674271179*x + 0.002304463491,
6.5:  lambda x: -3.145629739e-12*x**6 + 1.717125611e-09*x**5 - 3.764422141e-07*x**4 + 4.211829235e-05*x**3 - 0.002527115447*x**2 + 0.07743146769*x + 0.002774506345,
7.0:  lambda x: -3.15173756e-12*x**6 + 1.720847568e-09*x**5 - 3.773016417e-07*x**4 + 4.221135735e-05*x**3 - 0.00253173937*x**2 + 0.07750648778*x + 0.002912563345,
8.0:  lambda x: -3.015862386e-12*x**6 + 1.64832132e-09*x**5 - 3.625594994e-07*x**4 + 4.079038207e-05*x**3 - 0.002466978443*x**2 + 0.0763726388*x + 0.002408057416,
9.0:  lambda x: -2.754066272e-12*x**6 + 1.507839828e-09*x**5 - 3.338196735e-07*x**4 + 3.799899212e-05*x**3 - 0.002338743519*x**2 + 0.07412416185*x + 0.001293642605,
11.0: lambda x: -2.043571364e-12*x**6 + 1.126129997e-09*x**5 - 2.555490617e-07*x**4 + 3.036678891e-05*x**3 - 0.001985915923*x**2 + 0.06787698555*x - 0.001706466403,
12.0: lambda x: -1.657970641e-12*x**6 + 9.189045071e-10*x**5 - 2.129752032e-07*x**4 + 2.619683857e-05*x**3 - 0.001791531143*x**2 + 0.06438018819*x - 0.003213203245,
13.0: lambda x: -1.276534901e-12*x**6 + 7.139928882e-10*x**5 - 1.7083728e-07*x**4 + 2.20568029e-05*x**3 - 0.001597273057*x**2 + 0.06083761277*x - 0.004606805908,
14.0: lambda x: -1.276534901e-12*x**6 + 7.139928882e-10*x**5 - 1.7083728e-07*x**4 + 2.20568029e-05*x**3 - 0.001597273057*x**2 + 0.06083761277*x - 0.004606805908,
15.0: lambda x: -1.816099224e-08*x**4 + 6.566155209e-06*x**3 - 0.0008566921904*x**2 + 0.04721803398*x + 0.01197064697,
16.0: lambda x: -1.727742069e-08*x**4 + 6.252917467e-06*x**3 - 0.0008224471897*x**2 + 0.04604912174*x + 0.006732577491,
17.0: lambda x: -1.639295431e-08*x**4 + 5.939724646e-06*x**3 - 0.0007881338775*x**2 + 0.04486160615*x + 0.002016746411,
18.0: lambda x: -1.551795635e-08*x**4 + 5.630310254e-06*x**3 - 0.0007541821595*x**2 + 0.04367291195*x - 0.002276617433,
19.0: lambda x: 2.964452371e-11*x**5 - 2.79927888e-08*x**4 + 7.434309978e-06*x**3 - 0.0008579529289*x**2 + 0.04567096057*x - 0.01814528812,
20.0: lambda x: 7.928785091e-13*x**6 - 3.979798537e-10*x**5 + 5.947305978e-08*x**4 - 9.751431817e-07*x**3 - 0.0004801908831*x**2 + 0.03912636019*x - 0.01023350198
}

class System:

    intersection_depth = 0
    intersects_target = False
    photon_path = vec(0,0,0)
    neutron_path = (vec(0,0,0),vec(0,0,0))
    neutron_success = False
    n_theta_CM = 0
    n_phi_CM = 0
    polarization = 1
    p = 0   # momentum of the photon (MeV/c) Uninitialized until γE is sampled
    v = 0   # velocity of the CM frame
    γ = 0   # Lorentz factor

    # Derived momentum for neutron and proton in CM frame
    pn = 0

    def set_photon_path(self):
        """
        Generates a photon path of flight
        """
        self.p = E_lvl = γ_E_lvl_PDF_sampler().item()
        self.set_vars_of_p()
        sampler = get_sampler(E_lvl)
        theta = sampler().item()
        self.photon_path = sph_car(*(theta,rnd()*2*pi))*E_lvl # NOTE: Sampling range restricted from pi to theta max, since it's unnecessary to check photons that will never hit the target 
    
    def set_vars_of_p(self):
        self.v = self.p / (self.p + md)     # velocity of the CM frame
        self.γ = 1 / sqrt(1 - self.v**2)    # Lorentz factor

        # Derived momentum for neutron and proton in CM frame
        s = md**2 + 2 * md * self.p
        self.pn = sqrt(((s - (mp + mn)**2) * (s - (mp - mn)**2)) / (4 * s))

    def set_intersection_depth(self):
        """
        Initializes intersection depth
        """
        en, ex, hit = ray_through_aabb(self.photon_path, T_min, T_max)
        if hit and dot(en, vec(a0, a0, 1)) > 0:
            self.intersection_depth = norm3(en-ex)
            self.intersects_target = True
        else:
            self.intersection_depth = 0
            self.intersects_target = False

#-----------------------------------Check this out---------------------------------------
    
#----------------------------------------------------------------------------------------
# big breakthrough: most of this can be precomputed and cached. then because at that point everything
# going into ray_through_aabb is cached, we can precompute that suff too. This will be ~0.4x speedup
    def neutron_through_detector(self, detector):
        pos = None
        NP_temp = self.neutron_path[1]-self.neutron_path[0] # type: ignore
        if detector == '45':
            pos = D_45_pos-self.neutron_path[0]
        elif detector == '90':
            pos = D_90_pos-self.neutron_path[0]
        elif detector == '135':
            pos = D_135_pos-self.neutron_path[0]
        else:
            pos = D_155_pos-self.neutron_path[0]
        pos_new = rotate_point_to_vector(NP_temp.astype(float64), pos.astype(float64), True)
        min_bad, max_bad = D_minmax(pos_new) # rotated wrong
        c = vec((max_bad[0]+min_bad[0])/2,(max_bad[1]+min_bad[1])/2,(max_bad[2]+min_bad[2])/2)
        min_good = vec(c[0]-D_depth/2,min_bad[1],c[2]-D_width/2)
        max_good = vec(c[0]+D_depth/2,max_bad[1],c[2]+D_width/2)

        en, ex, hit = ray_through_aabb(vec(a0,a0,1), min_good, max_good) # for some reason, the aabb function can't handle perfectly axis-aligned rays, hence the 'a0'
        if hit and dot(en, vec(a0,a0,1)) > 0:
            return True  

    def set_neutron_path(self):
        """
        Generates a collision depth of and path/momentum of the neutron coming off of the γd->pn reaction. 
        Assumes a perfectly z-aligned path of travel for the photon, though this is corrected when rotating
        back in alignment with the actual photon direction. This is just done for simpler (and faster)
        computation.
        """
        # snap the photon energy to one defined in the dict data
        mev = mev_raw = norm3(self.photon_path)
        if mev <= 7:
            mev = round(mev * 2) / 2 # rounded to the nearest 0.5
        else:
            mev = round(mev) # round to the nearest 1
        mev = max(min(mev,20),3) # bound to defined range
        if mev == 10:
            mev = 9 if mev_raw < mev else 11

        # sample theta given photon energy and Arenhovel data
        thetaCM = uni(0,pi)
        while rnd() >= MeV_to_cross_section_by_theta[mev](thetaCM) / MeV_to_x_sect_max_value[mev]:
            thetaCM = uni(0,pi)
        self.n_theta_CM = thetaCM

        sigma_theta = MeV_to_photon_asymmetry_by_theta[mev](numpy.degrees(thetaCM))
        max_pdf = (1 + abs(self.polarization * sigma_theta)) / (2 * pi)
        phiCM = None
        while phiCM is None:
            phi = uni(0, 2*pi)
            y = uni (0, max_pdf)
            prob = (1 + self.polarization * sigma_theta * cos(2 * phi)) / (2 * pi)
            if y < prob:
                self.n_phi_CM = phiCM = phi

        EnCM = sqrt(self.pn**2 + mn**2)
        EnLab = self.γ*EnCM+self.v*self.γ*self.pn*cos(thetaCM)
        direction_imp = vec(self.pn*sin(thetaCM)*cos(phiCM),self.pn*sin(thetaCM)*sin(phiCM),self.v*self.γ*EnCM+self.γ*self.pn*cos(thetaCM))
        collision_depth = depth_sampler().item()
        poc_imp = vec(0,0,O_T_dist+collision_depth)
        self.neutron_path = (rotate_point_to_vector(self.photon_path.astype(float64),poc_imp.astype(float64)),rotate_point_to_vector(self.photon_path.astype(float64),direction_imp.astype(float64))) # I might take issue with rotating the CM direction about the photon path and leaving it at that. Will it make it so the neutron direction is still, in some respects, still in CM frame?

myclass = System()
lns1 = []
lns2 = []
lns3 = []
lns4 = []
hit_45 = 0
hit_90 = 0
hit_135 = 0
hit_155 = 0
loops = 10_000_000
percentage = 0
init_per_photon_sampling()
for i in range(loops):
    myclass.set_photon_path()
    myclass.set_intersection_depth()
    if myclass.intersects_target:
        # en, ex = ray_through_aabb(myclass.photon_path, T_min, T_max)
        # marker(en.flatten()) # type: ignore
        # marker(ex.flatten(),(1,0,0)) # type: ignore

        myclass.set_neutron_path()

        lns1.append(vector_to_list(myclass.neutron_path[0],array([0,0,0], dtype=float64), rescale=False))
        npath = vector_to_list(myclass.neutron_path[1],myclass.neutron_path[0],length=1000)
        if myclass.neutron_through_detector('90'):
            hit_90 += 1
            lns4.append(npath)
        elif myclass.neutron_through_detector('135'):
            hit_135 += 1
            lns4.append(npath)
        elif myclass.neutron_through_detector('155'):
            hit_155 += 1
            lns4.append(npath)
        elif myclass.neutron_through_detector('45'):
            hit_45 += 1
            lns4.append(npath)
        else:
            lns3.append(npath)

    else:
        lns2.append(vector_to_list(myclass.photon_path,array([0,0,0], dtype=float64),rescale=False))
    
    if (x := (i * 100) // loops) > percentage:
        print(f"{x}%", flush=True)
        percentage = x

print('printing scene...')

print(f"45: {hit_45}, 90: {hit_90}, 135: {hit_135}, 155: {hit_155}")

# line(lns1,(1,0,0))
# line(lns3,(0,1,0))
# line(lns4,(1,0.2,0.2))
# line(lns2,(1,1,1,0.05))

# print_scene()

# angles = []
# for npath in lns3 + lns4:  # lns3 (missed detector), lns4 (hit detector)
#     start, end = array(npath[0]), array(npath[1])  # Extract start and end points
#     direction = end - start  # Compute direction vector
#     theta = numpy.arctan2(direction[0], direction[2])  # Compute angle w.r.t. positive z-axis
#     angles.append(theta)  # Convert to degrees

# # Plot histogram
# plt.figure(figsize=(8, 6))
# plt.hist(angles, bins=30, edgecolor='black', alpha=0.7)
# plt.xlabel("Angle (rad)")
# plt.ylabel("Frequency")
# plt.title("Angular Distribution of Neutron Paths in x-z Plane")
# plt.grid(True)

# plt.show()

#--------------------------------------------------

# from collections import defaultdict

# energy_bin_edges = [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0,
#                     8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0,
#                     16.0, 17.0, 18.0, 19.0, 20.0]
# bin_centers = [(a + b)/2 for a, b in zip(energy_bin_edges[:-1], energy_bin_edges[1:])]

# # Initialize hit counters per bin index
# hit_counts_45 = defaultdict(int)
# hit_counts_90 = defaultdict(int)
# hit_counts_135 = defaultdict(int)
# hit_counts_155 = defaultdict(int)

# def find_bin_idx(energy):
#     for i in range(len(energy_bin_edges) - 1):
#         if energy_bin_edges[i] <= energy < energy_bin_edges[i + 1]:
#             return i
#     return None


# myclass = System()
# loops = 100000
# percentage = 0
# for i in range(loops):
#     myclass.set_photon_path()
#     photon_energy = norm3(myclass.photon_path)
    
#     myclass.set_intersection_depth()
#     if myclass.intersects_target:
#         myclass.set_neutron_path()
#         if myclass.neutron_path[0] is not None:

#             if myclass.neutron_through_detector('45'):
#                 hit_counts_45[find_bin_idx(photon_energy)] += 1
#             elif myclass.neutron_through_detector('90'):
#                 hit_counts_90[find_bin_idx(photon_energy)] += 1
#             elif myclass.neutron_through_detector('135'):
#                 hit_counts_135[find_bin_idx(photon_energy)] += 1
#             elif myclass.neutron_through_detector('155'):
#                 hit_counts_155[find_bin_idx(photon_energy)] += 1
#     if (x := (i * 100) // loops) > percentage:
#         print(f"{x}%", flush=True)
#         percentage = x

# energies = []
# ratios_135 = []
# ratios_155 = []
# ratios_45 = []

# for idx, E in enumerate(bin_centers):
#     c45 = hit_counts_45[idx]
#     c90 = hit_counts_90[idx]
#     c135 = hit_counts_135[idx]
#     c155 = hit_counts_155[idx]
    
#     if c90 > 0:
#         energies.append(E)
#         ratios_135.append(c135 / c90)
#         ratios_155.append(c155 / c90)
#         ratios_45.append(c45 / c90)

# print(hit_counts_45)
# print(hit_counts_90)
# print(hit_counts_135)
# print(hit_counts_155)

# # Plotting
# plt.figure(figsize=(10, 6))

# plt.plot(energies, ratios_135, label='σ(135°)/σ(90°)', marker='o')
# plt.plot(energies, ratios_155, label='σ(155°)/σ(90°)', marker='s')
# plt.plot(energies, ratios_45, label='σ(45°)/σ(90°)', marker='x')

# plt.xlabel("Photon Energy (MeV)")
# plt.ylabel("Cross Section Ratio")
# plt.title("Differential Cross Section Ratios vs Photon Energy")
# plt.legend()
# plt.grid(True)

# plt.tight_layout()
# plt.show()

"""
- For different directions of the neutron (theta) that comes out:  make a histogram for the number of neutrons as a function of momentum/energy
- What is the depth through target for each photon energy

Notes:
OLD
- I think there might be something fundamentally off with how we are generating photon distribution from source. I do not know what is the issue: 
Did I misremember the instructions? Are my approxomate PDFs wildly off? Is it actually fine? Was this broken from the very beginning? I do not know.
Below is my current algorithm for photon path generation, for future reference and debugging:
1. Get random evergy level of photon. We are working (at the moment) within the range [2.5, 20] MeV and we are drawing from the PDF f(x)=1/(x+0.1).
2. Use the energy level to generate the PDF for angular distribution at the randomly selected energy level.
3. Randomly select theta from the angular distribution PDF, [0, θ_max].
4. Randomly select phi in [0, 2pi].
- Note that I use this system where I select from two PDFs becuase, if I make theta directly correlated to energy level, then we get big holes in
angular distribution when looking over intervals. This felt like an error to me.
- For some reason, I'm not getting any neutrons produced.
- We don't get enough neutrons for very many detector intersections.
NEW
- Issues with increasing deuteron density. While we do get as many neutrons per photon as we could want, it comes at the cost of distorted...somethings. 
For instance, the expected probability for low density multiples (i.e. 0.0034 neutrons/photon ~ probability)
"""
