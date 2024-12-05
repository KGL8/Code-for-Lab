# routines.py
from imports import *

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
        E_lvl = sample_from_pdf(γ_E_lvl_PDF,*γErange)
        self.photon_path = sph_car(*(γ_E_to_θ(E_lvl),uni(0,2*pi)))
    
    def set_intersection_depth(self):
        """
        Initializes intersection depth
        """
        en, ex = ray_through_aabb(self.photon_path, T_min, T_max)
        if en is not None and ex is not None:
            self.intersection_depth = norm(en-ex)
            self.intersects_target = True

#-----------------------------------Check this out---------------------------------------

    def get_unpolarized_cs(self):
        if mev in MeV_to_cross_section_by_theta:
            return MeV_to_cross_section_by_theta[mev](theta)
        else:
            raise ValueError(f"No function defined for {mev} MeV")
        
    def T(theta):
        return 1
    
    def polarization_to_cs(self):
        return self.get_unpolarized_cs()*(1+self.polarization*T(self.n_theta_CM)*cos(2*self.n_phi_CM))
    
#----------------------------------------------------------------------------------------

    def neutron_path(self):
        """
        Generates a collision depth of and path/momentum of the neutron coming off of the γd->pn reaction. 
        Assumes a perfectly z-aligned path of travel for the photon, though this is corrected when rotating
        back in alignment with the actual photon direction. This is simply done for simpler (and faster)
        computation.
        """
        self.n_theta_CM = thetaCM = sample_from_pdf(nθCM_PDF,0,pi).item()
        self.n_phi_CM = phiCM = uni(0,2*pi)
        EnCM = sqrt(pn**2 + mn**2)
        EnLab = γ*EnCM+v*γ*pn*sin(thetaCM)*cos(phiCM)
        direction_imp = vec(pn*sin(thetaCM)*cos(phiCM),pn*sin(thetaCM)*sin(phiCM),v*γ*EnCM+γ*pn*cos(thetaCM))
        collision_depth = sample_from_pdf(γ_depth_PDF,0,self.intersection_depth).item()
        poc_imp = vec(0,0,O_T_dist+collision_depth)
        if self.polarization_to_cs() >= rnd():
            return (rotate_point_to_vector(self.photon_path,poc_imp),rotate_point_to_vector(self.photon_path,direction_imp))
        return (None,None)
    
myclass = System()