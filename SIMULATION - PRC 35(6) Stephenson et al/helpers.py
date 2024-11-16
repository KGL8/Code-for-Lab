# helpers.py
from imports import *

def sph_car(theta, phi, r=1):
    """
    Spherical coordinates to cartesian coordinates.

    Parameters:
    - theta: Angle away from z
    - phi: Angle around z
    - r: (optional) Distance from O

    Returns:
    - Vector
    """
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return array([x,y,z])

def sample_from_pdf(pdf, a, b, num_samples=1):
    """
    Generate random samples from a specified range [a, b] according to a non-normalized PDF.

    Parameters:
    - pdf: The non-normalized probability density function (PDF) to sample from.
    - a: The lower bound of the range.
    - b: The upper bound of the range.
    - num_samples: The number of samples to generate (default is 1).

    Returns:
    - An array of random samples from the specified range based on the PDF.
    """
    # Calculate the normalization constant
    normalization_constant, _ = quad(pdf, a, b)
    
    # Define the normalized PDF
    def normalized_pdf(x):
        return pdf(x) / normalization_constant
    
    # Create the cumulative distribution function (CDF)
    def cdf(x):
        return quad(normalized_pdf, a, x)[0]  # Integral from a to x
    
    # Generate uniform random samples
    uniform_samples = array([rnd() for _ in range(num_samples)])
    
    # Inverse transform sampling to get samples from the PDF
    samples = []
    for u in uniform_samples:
        # Use a numerical approach to find x such that cdf(x) = u
        low, high = a, b
        while high - low > 1e-5:  # Precision level
            mid = (low + high) / 2
            if cdf(mid) < u:
                low = mid
            else:
                high = mid
        samples.append(low)  # low is close to the value where cdf(low) = u

    return array(samples)

def ray_through_aabb(d, bmin, bmax):
    """
    Determines intersection points of ray through AABB. Assumes ray origin at (0,0,0).

    Parameters:
    - d: ray direction
    - bmin: minimum point on the box
    - bmax: maximum point on the bax

    Returns:
    - entry point, exit point
    """
    tmin, tmax = float('-inf'), float('inf')
    for i in range(3):
        t1 = bmin[i] / d[i]
        t2 = bmax[i] / d[i]
        tmin, tmax = max(tmin, min(t1, t2)), min(tmax, max(t1, t2))
        if tmin > tmax:
            return None, None
    return d * tmin, d * tmax\
    
def rotate_point_to_vector(v, point):
    v = v / norm(v)
    z_axis = array([0, 0, 1])
    rotation_axis = cross(z_axis, v)
    
    if allclose(rotation_axis, 0):
        return point
    
    rotation_axis /= norm(rotation_axis)
    angle = arccos(dot(z_axis, v))
    
    K = array([[0, -rotation_axis[2], rotation_axis[1]],
               [rotation_axis[2], 0, -rotation_axis[0]],
               [-rotation_axis[1], rotation_axis[0], 0]])
    
    rotation_matrix = eye(3) + sin(angle) * K + (1 - cos(angle)) * K @ K
    return rotation_matrix @ point
