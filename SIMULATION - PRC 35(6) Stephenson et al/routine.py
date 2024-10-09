# routines.py
from imports import *

class System:

    depth_through_target = 0

    @staticmethod
    def nθCM_PDF(x):
        return 3/(x**2+1)
    
    @staticmethod
    def γ_depth_PDF(x):
        return 1/(2*x+1)

    def neutron_path(self):
        """
        Generates a collision depth of and path/momentum of the neutron coming off of the γd->pn reaction. 
        Assumes a perfectly z-aligned path of travel for the photon, though this is corrected when rotating
        back in alignment with the actual photon direction. This is simply done for simpler (and faster)
        computation.

        Parameters:
        - Photon: distance traveled through target (along ACTUAL path of travel)
 
        Returns: 
        - Tuple(Vec3,Vec3) -- (Point of Collision, Neutron Momentum)
        """
        thetaCM = sample_from_pdf(self.nθCM_PDF,0,pi).item()
        phiCM = uni(0,2*pi)
        EnCM = sqrt(pn**2 + mn**2)
        EnLab = γ*EnCM+v*γ*pn*sin(thetaCM)*cos(phiCM)
        direction = vec(pn*sin(thetaCM)*cos(phiCM),pn*sin(thetaCM)*sin(phiCM),v*γ*EnCM+γ*pn*cos(thetaCM))
        collision_depth = sample_from_pdf(self.γ_depth_PDF,0,self.depth_through_target).item()
        poc = vec(0,0,O_T_dist+collision_depth)
        return (poc,direction)

myclass = System()
myclass.depth_through_target = 4
print(myclass.neutron_path())