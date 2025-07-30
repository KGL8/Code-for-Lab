# helpers.py
from imports import *
import numpy as np
from numba import njit

def vector_to_list(vec, start, length=1, rescale=True):
    """
    Vector to Vispy-friendly format

    Parameters:
    - vec: Ndarray for directon
    - length: desired length after rescaling
    - rescale: Do you want to normalize the vector length?
    """
    vx, vy, vz = vec[0] - start[0], vec[1] - start[1], vec[2] - start[2]

    if rescale:
        mag = sqrt(vx*vx + vy*vy + vz*vz)
        if mag != 0.0:
            inv_mag = length / mag
            vx *= inv_mag
            vy *= inv_mag
            vz *= inv_mag
    else:
        vx *= length
        vy *= length
        vz *= length

    return [
        [start[0], start[1], start[2]],
        [start[0] + vx, start[1] + vy, start[2] + vz]
    ]

def sph_car(theta, phi, r=1.0):
    """
    Spherical coordinates to cartesian coordinates.

    Parameters:
    - theta: Angle away from z
    - phi: Angle around z
    - r: (optional) Distance from O

    Returns:
    - Vector
    """
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x,y,z], dtype=np.float64)

# ---------- CACHED SAMPLING SYSTEM ----------
def build_sampler(pdf_fn, a, b, grid_size=500):
    dx = (b - a) / (grid_size - 1)
    x_vals = numpy.linspace(a, b, grid_size)

    # Evaluate and normalize PDF
    pdf_vals = pdf_fn(x_vals)
    pdf_vals /= (pdf_vals[0] + pdf_vals[-1] + 2 * pdf_vals[1:-1].sum()) * dx * 0.5

    # Compute CDF
    cdf_vals = numpy.empty_like(pdf_vals)
    cdf_vals[0] = 0.0
    cdf_vals[1:] = dx * (0.5 * (pdf_vals[:-1] + pdf_vals[1:])).cumsum()
    cdf_vals /= cdf_vals[-1]

    # Return the sampler function
    def sampler(num_samples=1):
        return numpy.interp(numpy.random.rand(num_samples), cdf_vals, x_vals)

    return sampler


@njit
def ray_through_aabb(d, bmin, bmax):
    # Reject downward-facing rays (your temporary condition)
    if d[2] < 0:
        return np.empty(3, dtype=np.float64), np.empty(3, dtype=np.float64), False

    tmin = -1e20
    tmax = 1e20

    for i in range(3):
        if d[i] == 0:
            if bmin[i] < 0 or bmax[i] < 0:
                return np.empty(3, dtype=np.float64), np.empty(3, dtype=np.float64), False
            continue
        t1 = bmin[i] / d[i]
        t2 = bmax[i] / d[i]
        tmin = max(tmin, min(t1, t2))
        tmax = min(tmax, max(t1, t2))
        if tmin > tmax:
            return np.empty(3, dtype=np.float64), np.empty(3, dtype=np.float64), False

    entry = d * tmin
    exit = d * tmax
    return entry, exit, True


# def ray_through_aabb_old(d, bmin, bmax):
#     """
#     Determines intersection points of ray through AABB. Assumes ray origin at (0,0,0).

#     Parameters:
#     - d: ray direction
#     - bmin: minimum point on the box
#     - bmax: maximum point on the box

#     Returns:
#     - entry point, exit point
#     """

#     # temporary? ###############
#     if d[2] < 0:
#         return None, None
#     ############################
    
#     tmin, tmax = float('-inf'), float('inf')
#     for i in range(3):
#         if d[i] == 0:
#             t1 = float('inf')
#             t2 = float('inf')
#             if bmin[i] < 0:
#                 t1 = float('-inf')
#             if bmax[i] < 0:
#                 t2 = float('-inf')
#         else:
#             t1 = bmin[i] / d[i]
#             t2 = bmax[i] / d[i]
#         tmin, tmax = max(tmin, min(t1, t2)), min(tmax, max(t1, t2))
#         if tmin > tmax or tmax == float('inf') or tmax == float('-inf'):
#             return None, None
#     return d * tmin, d * tmax

@njit
def norm3(v):
    return (v[0]**2 + v[1]**2 + v[2]**2)**0.5

@njit
def vec3_cross(a, b):
    return np.array([
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ], dtype=np.float64)

@njit
def vec3_allclose(a, b, rtol=1e-5, atol=1e-8):
    return (
        abs(a[0] - b[0]) <= atol + rtol * abs(b[0]) and
        abs(a[1] - b[1]) <= atol + rtol * abs(b[1]) and
        abs(a[2] - b[2]) <= atol + rtol * abs(b[2])
    )

@njit
def rotate_point_to_vector(v, point, opposite=False):
    v_len = norm3(v)
    if v_len == 0.0:
        return point.astype(np.float64)
    v = v / v_len

    z_axis = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    neg_z_axis = np.array([0.0, 0.0, -1.0], dtype=np.float64)

    if vec3_allclose(v, z_axis):
        return point.astype(np.float64)
    elif vec3_allclose(v, neg_z_axis):
        return (-point if not opposite else point).astype(np.float64)

    axis = vec3_cross(z_axis, v)
    axis_len = norm3(axis)
    if axis_len == 0.0:
        return point.astype(np.float64)
    axis = axis / axis_len

    angle = np.arccos(v[2])
    if opposite:
        angle = -angle

    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)

    k = axis
    px, py, pz = point
    kx, ky, kz = k

    dot_kp = kx*px + ky*py + kz*pz
    cross = vec3_cross(k, point)

    out = (
        point * cos_theta +
        cross * sin_theta +
        k * dot_kp * (1.0 - cos_theta)
    )

    return out.astype(np.float64)

## For testing ##############################################

# def rotate_point_to_vector_ref(v, point, opposite=False):
#     """
#     Rotates a point such that it is the same relative to 'v' as it was the z-axis

#     Parameters:
#     - v: vector the point is rotated around to
#     - point: point

#     Returns:
#     - rotated point
#     """
#     v = asarray(v, dtype=float32)
#     point = asarray(point, dtype=float32)

#     v_len = norm(v)
#     if v_len == 0:
#         return point
#     v /= v_len

#     z_axis = array([0.0, 0.0, 1.0])

#     if allclose(v, z_axis):
#         return point
#     elif allclose(v, -z_axis):
#         return -point if not opposite else point

#     # Rotation axis: ẑ × v
#     axis = numpy.cross(z_axis, v)
#     axis_norm = norm(axis)
#     if axis_norm == 0:
#         return point
#     axis = axis / axis_norm

#     # Angle: arccos(ẑ ⋅ v)
#     angle = arccos(v[2])
#     if opposite:
#         angle = -angle

#     # Rodrigues' rotation formula applied directly
#     cos_theta = cos(angle)
#     sin_theta = sin(angle)
#     k = axis
#     kx, ky, kz = k
#     px, py, pz = point

#     dot_kp = kx*px + ky*py + kz*pz
#     cross = numpy.cross(k, point)

#     out = (
#         point * cos_theta +
#         cross * sin_theta +
#         k * dot_kp * (1 - cos_theta)
#     )

#     return out
