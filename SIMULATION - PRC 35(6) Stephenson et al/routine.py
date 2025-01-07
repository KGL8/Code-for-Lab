# routines.py
from imports import *
from interface import *

# angle (rad) to differential cross section at various photon energies (Lab)
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

class System:

    intersection_depth = 0
    intersects_target = False
    photon_path = vec(0,0,0)
    neutron_success = False
    n_theta_CM = 0
    n_phi_CM = 0
    polarization = 0


    def set_photon_path(self):
        """
        Generates a photon path of flight
        """
        E_lvl = sample_from_pdf(γ_E_lvl_PDF,*γErange).item()
        γ_E_to_θ_PDF_sv = lambda x: γ_E_to_θ_PDF(x=x,e=E_lvl)
        self.photon_path = sph_car(*(sample_from_pdf(γ_E_to_θ_PDF_sv,*(0,pi)).item(),0))*E_lvl
    
    def set_intersection_depth(self):
        """
        Initializes intersection depth
        """
        en, ex = ray_through_aabb(self.photon_path, T_min, T_max)
        if en is not None and ex is not None:
            self.intersection_depth = norm(en-ex)
            self.intersects_target = True
        else:
            self.intersection_depth = 0
            self.intersects_target = False

#-----------------------------------Check this out---------------------------------------

    def get_unpolarized_cs(self):
        if mev in MeV_to_cross_section_by_theta:
            return MeV_to_cross_section_by_theta[mev](theta)
        else:
            raise ValueError(f"No function defined for {mev} MeV")
    
    def polarization_to_cs(self):
        return self.get_unpolarized_cs()*(1+self.polarization*cos(self.n_phi_CM))
    
#----------------------------------------------------------------------------------------

    def neutron_path(self):
        """
        Generates a collision depth of and path/momentum of the neutron coming off of the γd->pn reaction. 
        Assumes a perfectly z-aligned path of travel for the photon, though this is corrected when rotating
        back in alignment with the actual photon direction. This is just done for simpler (and faster)
        computation.
        """
        self.n_theta_CM = thetaCM = sample_from_pdf(nθCM_PDF,0,pi).item()
        self.n_phi_CM = phiCM = uni(0,2*pi)
        if self.polarization_to_cs() >= rnd():
            EnCM = sqrt(pn**2 + mn**2)
            EnLab = γ*EnCM+v*γ*pn*sin(thetaCM)*cos(phiCM)
            direction_imp = vec(pn*sin(thetaCM)*cos(phiCM),pn*sin(thetaCM)*sin(phiCM),v*γ*EnCM+γ*pn*cos(thetaCM))
            collision_depth = sample_from_pdf(γ_depth_PDF,0,self.intersection_depth).item()
            poc_imp = vec(0,0,O_T_dist+collision_depth)
            return (rotate_point_to_vector(self.photon_path,poc_imp),rotate_point_to_vector(self.photon_path,direction_imp))
        return (None,None)
    
myclass = System()
lns = []
for i in range(1000000):
    myclass.set_photon_path()
    lns.append([[0,0,0],(myclass.photon_path).tolist()])
    # myclass.set_intersection_depth()
    # if myclass.intersects_target:
    #     en, ex = ray_through_aabb(myclass.photon_path, T_min, T_max)
    #     marker(en.flatten()) # type: ignore
    #     marker(ex.flatten(),(1,0,0)) # type: ignore
    #     line(vector_to_list(myclass.photon_path,15),(1,0,0,0.5))
    # else:
    #     # line(vector_to_list(myclass.photon_path,15),(1,1,1,0.5))
    #     pass
line(lns,(1,1,1,0.5))
line([[0,0,0], sph_car(0,0,100).tolist()], (0,1,1))
print_scene()

"""
- For different directions of the neutron (theta) that comes out:  make a histogram for the number of neutrons as a function of momentum/energy
- 

Notes:
- I think there might be something fundamentally off with how we are generating photon distribution from source. I do not know what is the issue: 
Did I misremember the instructions? Are my approxomate PDFs wildly off? Is it actually fine? Was this broken from the very beginning? I do not know.
Below is my current algorithm for photon path generation, for future reference and debugging:
1. Get random evergy level of photon. We are working (at the moment) within the range [2.5, 20] MeV and we are drawing from the PDF f(x)=1/(x+0.1).
2. Use the energy level to generate the PDF for angular distribution at the randomly selected energy level.
3. Randomly select theta from the angular distribution PDF, [0, pi].
4. Randomly select phi in [0, 2pi].
- Note that I use this system where I select from two PDFs becuase, if I make theta directly correlated to energy level, then we get big holes in
angular distribution when looking over intervals. This felt like an error to me.
"""