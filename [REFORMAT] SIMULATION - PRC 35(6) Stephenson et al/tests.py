# # tests.py
from imports import *
# from interface import * # type: ignore


# merge lines into a list for way way way faster rendering. like 10000x faster. all lines in a group must be the same color, though.
# lns = []
# hits = []
# for k in range(100000):
#     o = [0,0,0]
#     d = [(rnd()-0.5)*30,(rnd()-0.5)*30,(rnd()-0.5)*100]
#     en, ex = ray_through_aabb(array(d),T_min,T_max)
#     if en is not None and ex is not None:
#         hits.append([o,d])
#     else:
#         lns.append([o,d])
# line(hits,(1/2,0,0,1/2))
# line(lns,(1,1,1,0.01))
# print_scene()

# data = []
# for i in range(100000):
#     data.append(sample_from_pdf(γ_E_lvl_PDF,*γErange).item())

# plt.hist(data, bins=30, color='skyblue', edgecolor='black')

# plt.xlabel('Energy Level')
# plt.ylabel('Frequency')

# plt.show()

# dat = [1, 2, 3, 4, 5]
# dat2 = [10, 15, 7, 12, 20]

# # Create scatter plot
# plt.scatter(dat, dat2, color='blue', marker='o', label="Data Points")

# # Labels and title
# plt.xlabel("dat")
# plt.ylabel("dat2")
# plt.title("Scatter Plot of dat vs. dat2")

# # Show legend
# plt.legend()

# # Display plot
# plt.show()

# # γ_E_to_θ_PDF_sv = lambda x: γ_E_to_θ_PDF(x=x,e=E_lvl)
# # print(sample_from_pdf(γ_E_to_θ_PDF_sv,*(0,pi/2)).item())

# import numpy as np
# import matplotlib.pyplot as plt

# dat = []
# dat2 = []
# for i in range(100000):
#     myclass.set_photon_path()
#     myclass.set_intersection_depth()
#     if myclass.intersects_target:
#         dat.append(myclass.intersection_depth)
#         dat2.append(np.sqrt(myclass.photon_path.dot(myclass.photon_path)))

# # Convert lists to numpy arrays for easier manipulation
# dat = np.array(dat)
# dat2 = np.array(dat2)

# # Create scatter plot
# plt.figure(figsize=(8, 6))
# plt.scatter(dat2, dat, color='blue', marker='o', alpha=0.3, label="Photon Intersections")

# # Apply log scale to depth (X-axis)
# plt.yscale("log")

# # Labels and title
# plt.ylabel("Depth (log scale)")
# plt.xlabel("Energy")
# plt.title("Scatter Plot with Histogram Overlay")

# # Bin the energy values
# num_bins = 20  # Adjust for resolution
# bins = np.linspace(min(dat2), max(dat2), num_bins)

# # Compute average intersection depth per bin
# bin_indices = np.digitize(dat2, bins)  # Assign each data point to a bin
# avg_depths = [np.mean(dat[bin_indices == i]) if np.any(bin_indices == i) else 0 for i in range(1, len(bins))]

# # Plot histogram overlay
# plt.bar(bins[:-1], avg_depths, width=np.diff(bins), align='edge', alpha=0.5, color='red', label="Avg. Depth per Energy Bin")

# # Show legend
# plt.legend()

# # Display plot
# plt.show()

#not quite working, idk why

#---------------------------------------------------------------------
#---------------------------------------------------------------------

# from numpy import sin, pi, allclose
# from scipy.stats import ks_2samp
# from numpy import linspace, interp, array, histogram
# from numpy.random import rand
# from scipy.integrate import trapezoid, cumulative_trapezoid
# from functools import lru_cache, wraps

# # ---------- ORIGINAL UNOPTIMIZED SAMPLER ----------
# def sample_from_pdf(pdf, a, b, num_samples=1, grid_size=500):
#     x_vals = linspace(a, b, grid_size)
#     pdf_vals = array([pdf(x) for x in x_vals])
#     normalization_constant = trapezoid(pdf_vals, x_vals)
#     pdf_vals /= normalization_constant
#     cdf_vals = cumulative_trapezoid(pdf_vals, x_vals, initial=0)
#     cdf_vals /= cdf_vals[-1]
#     uniform_samples = rand(num_samples)
#     return interp(uniform_samples, cdf_vals, x_vals)

# # ---------- CACHED SAMPLING SYSTEM ----------
# def precached_sampler(grid_size=500):
#     def decorator(pdf_fn):
#         @lru_cache(maxsize=128)
#         def make_cached_sampler(a, b):
#             x_vals = linspace(a, b, grid_size)
#             pdf_vals = array([pdf_fn(x) for x in x_vals])
#             pdf_vals /= trapezoid(pdf_vals, x_vals)
#             cdf_vals = cumulative_trapezoid(pdf_vals, x_vals, initial=0)
#             cdf_vals /= cdf_vals[-1]
#             def sampler(num_samples=1):
#                 return interp(rand(num_samples), cdf_vals, x_vals)
#             return sampler

#         @wraps(pdf_fn)
#         def wrapper(a, b, num_samples=1):
#             return make_cached_sampler(a, b)(num_samples)

#         return wrapper
#     return decorator

# # ---------- TEST CASE: SMOOTH PDF ----------
# def reference_pdf(x):
#     return 0.8 + 0.2*sin(3 * x)

# @precached_sampler(grid_size=500)
# def cached_pdf(x):
#     return 0.8 + 0.2*sin(3 * x)

# # ---------- RUN COMPARISON ----------
# def main():
#     a, b = 0, pi
#     num_samples = 1

#     samples_orig = sample_from_pdf(reference_pdf, a, b, num_samples)
#     samples_cached = cached_pdf(a, b, num_samples)
#     print(samples_cached)
#     print(samples_cached.item())
#     # # Kolmogorov-Smirnov test for distribution equality
#     # ks_stat, p_val = ks_2samp(samples_orig, samples_cached)

#     # print("KS Statistic:", f"{ks_stat:.5f}")
#     # print("p-value:     ", f"{p_val:.5f}")
#     # print("Distributions Match:", "YES" if p_val > 0.05 else "NO")

#     # # --- Extra test: PDF vs histogram correlation ---
#     # from scipy.stats import pearsonr

#     # bin_edges = linspace(a, b, 100)
#     # bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
#     # true_pdf_vals = array([reference_pdf(x) for x in bin_centers])
#     # true_pdf_vals /= trapezoid(true_pdf_vals, bin_centers)  # normalize

#     # hist_counts, _ = histogram(samples_cached, bins=bin_edges, density=True)

#     # corr, _ = pearsonr(true_pdf_vals, hist_counts)

#     # print("PDF Shape Correlation (cached):", f"{corr:.4f}")
#     # print("Shape Match:", "YES" if corr > 0.95 else "NO")

#     # # Optional histogram plot
#     # try:
#     #     import matplotlib.pyplot as plt
#     #     plt.hist(samples_orig, bins=100, alpha=0.5, label="original", density=True)
#     #     plt.hist(samples_cached, bins=100, alpha=0.5, label="cached", density=True)
#     #     plt.plot(bin_centers, true_pdf_vals, 'k--', label="true PDF")
#     #     plt.legend()
#     #     plt.title("PDF Sampling Comparison")
#     #     plt.show()
#     # except ImportError:
#     #     pass


# if __name__ == "__main__":
#     main()

# import numpy as np

# def vec3_allclose(a, b, rtol=1e-5, atol=1e-8):
#     return all(abs(a[i] - b[i]) <= atol + rtol * abs(b[i]) for i in range(3))

# def run_allclose_equivalence_test(N=1_000_000, seed=42):
#     np.random.seed(seed)
#     failures = 0

#     for _ in range(N):
#         # Random vec3s with wide range of magnitudes
#         scale = 10 ** np.random.uniform(-10, 10)
#         a = np.random.randn(3) * scale
#         b = a + np.random.randn(3) * 1e-9  # Slight noise

#         ref = np.allclose(a, b)
#         test = vec3_allclose(a, b)

#         if ref != test:
#             print(f"Mismatch:\n  a: {a}\n  b: {b}\n  np.allclose: {ref}, vec3_allclose: {test}")
#             failures += 1

#     if failures == 0:
#         print(f"✅ Passed: {N} comparisons match perfectly with np.allclose.")
#     else:
#         print(f"❌ {failures} mismatches found out of {N} tests.")

# if __name__ == "__main__":
#     run_allclose_equivalence_test()


# import numpy as np
# import matplotlib.pyplot as plt

# mp = 938.28     # mass of proton (MeV/c^2)
# mn = 939.57     # mass of neutron (MeV/c^2)
# md = 1875.61    # mass of deuteron (MeV/c^2)

# p_vals = np.linspace(10, 10000, 1000)  # photon momentum values

# v = p_vals / (p_vals + md)
# γ = 1 / np.sqrt(1 - v**2)
# EγCM = γ * p_vals * (1 - v)
# a = EγCM + md

# # Method 1
# pn_1 = np.sqrt(((a**2 + mn**2 - mp**2)**2 - 4 * a**2 * mn**2) / (4 * a**2))

# # Method 2
# s = md**2 + 2 * md * p_vals
# pn_2 = np.sqrt(((s - (mp + mn)**2) * (s - (mp - mn)**2)) / (4 * s))

# # Compare
# diff = np.abs(pn_1 - pn_2)
# rel_diff = diff / pn_1

# # Plot
# plt.plot(p_vals, rel_diff)
# plt.xlabel("Photon momentum p (MeV/c)")
# plt.ylabel("Relative difference between pn_1 and pn_2")
# plt.title("Relative difference: |pn_1 - pn_2| / pn_1")
# plt.grid()
# plt.show()

# # Optional: print max error
# print("Max relative error:", np.max(rel_diff))


# angle (rad) to differential cross section at various photon energies
# MeV_to_cross_section_by_theta = {
# 3:   lambda x: 0.009476*sin(2*x-1.532)+0.01153,
# 3.5: lambda x: 0.01259*sin(2*x-1.521)+0.01406,
# 4:   lambda x: 0.01385*sin(2.001*x-1.512)+0.015,
# 4.5: lambda x: 0.01411*sin(2.001*x-1.504)+0.01506,
# 5:   lambda x: 0.01385*sin(2.001*x-1.498)+0.01466,
# 5.5: lambda x: 0.01333*sin(2.001*x-1.491)+0.01405,
# 6:   lambda x: 0.01269*sin(2.001*x-1.485)+0.01334,
# 6.5: lambda x: 0.01201*sin(2.001*x-1.479)+0.01262,
# 7:   lambda x: 0.01134*sin(2.001*x-1.474)+0.01191,
# 8:   lambda x: 0.01007*sin(2.001*x-1.464)+0.01059,
# 9:   lambda x: 0.008947*sin(2.001*x-1.454)+0.009441,
# 11:  lambda x: 0.007149*sin(2.001*x-1.436)+0.007621,
# 12:  lambda x: 0.006437*sin(2.001*x-1.427)+0.006906,
# 13:  lambda x: 0.005821*sin(2.001*x-1.419)+0.00629,
# 14:  lambda x: 0.005288*sin(2*x-1.41)+0.005758,
# 15:  lambda x: 0.004824*sin(2*x-1.401)+0.005297,
# 16:  lambda x: 0.004416*sin(2*x-1.392)+0.004892,
# 17:  lambda x: 0.004058*sin(1.999*x-1.384)+0.004536,
# 18:  lambda x: 0.003741*sin(1.998*x-1.375)+0.004222,
# 19:  lambda x: 0.003459*sin(1.997*x-1.366)+0.003942,
# 20:  lambda x: 0.003207*sin(1.996*x-1.357)+0.003693
# }
# # peaks of the above sinusoidal functions
# MeV_to_x_sect_max_value = {
# 3:   0.009476 + 0.01153,
# 3.5: 0.01259 + 0.01406,
# 4:   0.01385 + 0.015,
# 4.5: 0.01411 + 0.01506,
# 5:   0.01385 + 0.01466,
# 5.5: 0.01333 + 0.01405,
# 6:   0.01269 + 0.01334,
# 6.5: 0.01201 + 0.01262,
# 7:   0.01134 + 0.01191,
# 8:   0.01007 + 0.01059,
# 9:   0.008947 + 0.009441,
# 11:  0.007149 + 0.007621,
# 12:  0.006437 + 0.006906,
# 13:  0.005821 + 0.00629,
# 14:  0.005288 + 0.005758,
# 15:  0.004824 + 0.005297,
# 16:  0.004416 + 0.004892,
# 17:  0.004058 + 0.004536,
# 18:  0.003741 + 0.004222,
# 19:  0.003459 + 0.003942,
# 20:  0.003207 + 0.003693
# }
# # angle (theta) to photon asymmetry at various photon energies
# # Notes: This takes theta in degrees because the arenhovel data takes theta in degrees,
# # and I literally just forgot to convert before performing the tedious task of fitting
# # polynomials to the data. Fyi, despite the regression saying these all match with
# # R^2 >= 0.995, there are sone pretty grossly unfitting functions in the teens,
# # particularly those of degree 4. The world is messy, so if the R^2 is good enough
# # then whatever.
# MeV_to_photon_asymmetry_by_theta = {
# 3.0:  lambda x: 1.521183874e-12*x**6 - 8.113529748e-10*x**5 + 1.508797309e-07*x**4 - 1.085486832e-05*x**3 + 4.333373917e-05*x**2 + 0.02825288912*x - 0.01174708966,
# 3.5:  lambda x: -1.738446179e-08*x**4 + 6.272217735e-06*x**3 - 0.0008237682169*x**2 + 0.04636448864*x - 0.002132951945,
# 4.0:  lambda x: -1.334758305e-12*x**6 + 7.363500359e-10*x**5 - 1.734752668e-07*x**4 + 2.21240491e-05*x**3 - 0.00159328487*x**2 + 0.06087277177*x - 0.005972614104,
# 4.5:  lambda x: -2.10536374e-12*x**6 + 1.153453998e-09*x**5 - 2.598564961e-07*x**4 + 3.065914771e-05*x**3 - 0.001994656474*x**2 + 0.06810291596*x - 0.002651288538,
# 5.0:  lambda x: -2.594467253e-12*x**6 + 1.418196942e-09*x**5 - 3.145901469e-07*x**4 + 3.604274466e-05*x**3 - 0.002245527588*x**2 + 0.072536132*x - 0.0002549764926,
# 5.5:  lambda x: -2.895597583e-12*x**6 + 1.581285458e-09*x**5 - 3.482953665e-07*x**4 + 3.935156128e-05*x**3 - 0.002399002566*x**2 + 0.07521869468*x + 0.001320771375,
# 6.0:  lambda x: -3.068266254e-12*x**6 + 1.674986449e-09*x**5 - 3.676888881e-07*x**4 + 4.125591406e-05*x**3 - 0.002487119015*x**2 + 0.07674271179*x + 0.002304463491,
# 6.5:  lambda x: -3.145629739e-12*x**6 + 1.717125611e-09*x**5 - 3.764422141e-07*x**4 + 4.211829235e-05*x**3 - 0.002527115447*x**2 + 0.07743146769*x + 0.002774506345,
# 7.0:  lambda x: -3.15173756e-12*x**6 + 1.720847568e-09*x**5 - 3.773016417e-07*x**4 + 4.221135735e-05*x**3 - 0.00253173937*x**2 + 0.07750648778*x + 0.002912563345,
# 8.0:  lambda x: -3.015862386e-12*x**6 + 1.64832132e-09*x**5 - 3.625594994e-07*x**4 + 4.079038207e-05*x**3 - 0.002466978443*x**2 + 0.0763726388*x + 0.002408057416,
# 9.0:  lambda x: -2.754066272e-12*x**6 + 1.507839828e-09*x**5 - 3.338196735e-07*x**4 + 3.799899212e-05*x**3 - 0.002338743519*x**2 + 0.07412416185*x + 0.001293642605,
# 11.0: lambda x: -2.043571364e-12*x**6 + 1.126129997e-09*x**5 - 2.555490617e-07*x**4 + 3.036678891e-05*x**3 - 0.001985915923*x**2 + 0.06787698555*x - 0.001706466403,
# 12.0: lambda x: -1.657970641e-12*x**6 + 9.189045071e-10*x**5 - 2.129752032e-07*x**4 + 2.619683857e-05*x**3 - 0.001791531143*x**2 + 0.06438018819*x - 0.003213203245,
# 13.0: lambda x: -1.276534901e-12*x**6 + 7.139928882e-10*x**5 - 1.7083728e-07*x**4 + 2.20568029e-05*x**3 - 0.001597273057*x**2 + 0.06083761277*x - 0.004606805908,
# 14.0: lambda x: -1.276534901e-12*x**6 + 7.139928882e-10*x**5 - 1.7083728e-07*x**4 + 2.20568029e-05*x**3 - 0.001597273057*x**2 + 0.06083761277*x - 0.004606805908,
# 15.0: lambda x: -1.816099224e-08*x**4 + 6.566155209e-06*x**3 - 0.0008566921904*x**2 + 0.04721803398*x + 0.01197064697,
# 16.0: lambda x: -1.727742069e-08*x**4 + 6.252917467e-06*x**3 - 0.0008224471897*x**2 + 0.04604912174*x + 0.006732577491,
# 17.0: lambda x: -1.639295431e-08*x**4 + 5.939724646e-06*x**3 - 0.0007881338775*x**2 + 0.04486160615*x + 0.002016746411,
# 18.0: lambda x: -1.551795635e-08*x**4 + 5.630310254e-06*x**3 - 0.0007541821595*x**2 + 0.04367291195*x - 0.002276617433,
# 19.0: lambda x: 2.964452371e-11*x**5 - 2.79927888e-08*x**4 + 7.434309978e-06*x**3 - 0.0008579529289*x**2 + 0.04567096057*x - 0.01814528812,
# 20.0: lambda x: 7.928785091e-13*x**6 - 3.979798537e-10*x**5 + 5.947305978e-08*x**4 - 9.751431817e-07*x**3 - 0.0004801908831*x**2 + 0.03912636019*x - 0.01023350198
# }

# import numpy as np
# import matplotlib.pyplot as plt

# from mpl_toolkits.mplot3d import Axes3D
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

# mev = mev_raw = uni(3,20)
# if mev <= 7:
#     mev = round(mev * 2) / 2 # rounded to the nearest 0.5
# else:
#     mev = round(mev) # round to the nearest 1
# mev = max(min(mev,20),3) # bound to defined range
# if mev == 10:
#     mev = 9 if mev_raw < mev else 11

# # P = 0

# # thetaCM = uni(0,pi)
# # while rnd() >= MeV_to_cross_section_by_theta[mev](thetaCM) / MeV_to_x_sect_max_value[mev]:
# #     thetaCM = uni(0,pi)

# # sigma_theta = MeV_to_photon_asymmetry_by_theta[mev](thetaCM)
# # max_pdf = (1 + abs(P * sigma_theta)) / (2 * pi)
# # phiCM = None
# # while phiCM is None:
# #     phi = uni(0, 2*pi)
# #     y = uni (0, max_pdf)
# #     prob = (1 + P * sigma_theta * cos(2 * phi)) / (2 * pi)
# #     if y < prob:
# #         phiCM = phi

# # Constants
# P_lin = 0

# # Cross-section components
# # def sigma_0(theta):
# #     return np.sin(theta)**2

# # def Sigma(theta):
# #     return np.cos(theta)

# # Grid: medium-res for performance
# theta = np.linspace(0, np.pi, 60)
# phi = np.linspace(0, 2 * np.pi, 60)
# THETA, PHI = np.meshgrid(theta, phi)

# # Evaluate distribution
# F = MeV_to_cross_section_by_theta[mev](THETA) * (1 + P_lin * MeV_to_photon_asymmetry_by_theta[mev](np.degrees(THETA)) * np.cos(2 * PHI))
# F /= np.max(F)  # normalize for color scaling

# # Convert to Cartesian coords on unit sphere
# X = np.sin(THETA) * np.cos(PHI)
# Y = np.sin(THETA) * np.sin(PHI)
# Z = np.cos(THETA)

# # Setup plot
# fig = plt.figure(figsize=(8, 6))
# ax = fig.add_subplot(111, projection='3d')

# # Plot surface with color, no lighting
# surface = ax.plot_surface(
#     X, Y, Z,
#     facecolors=plt.cm.viridis(F),
#     rstride=1, cstride=1,
#     antialiased=False,
#     shade=False,
#     linewidth=0,
#     edgecolor='none'
# )

# # Axis limits
# ax.set_xlim([-1.1, 1.1])
# ax.set_ylim([-1.1, 1.1])
# ax.set_zlim([-1.1, 1.1])

# # Axis labels and arrows
# arrow_len = 1.2
# ax.quiver(0,0,0, arrow_len,0,0, color='r', linewidth=1.5)
# ax.quiver(0,0,0, 0,arrow_len,0, color='g', linewidth=1.5)
# ax.quiver(0,0,0, 0,0,arrow_len, color='b', linewidth=1.5)
# ax.text(1.3, 0, 0, 'x', color='r')
# ax.text(0, 1.3, 0, 'y', color='g')
# ax.text(0, 0, 1.3, 'z', color='b')

# # View & aesthetics
# ax.view_init(elev=30, azim=135)
# ax.set_box_aspect([1,1,1])
# ax.set_title('Angular Distribution on Unit Sphere')
# ax.axis('off')

# plt.tight_layout()
# plt.show()

############################################
############################################
############################################
# import numpy as np
# from numpy import sin, cos, arccos, dot, eye, array
# import dash
# from dash import dcc, html, Output, Input
# import dash_daq as daq
# import plotly.graph_objects as go

# nrm = None

# # Your functions
# def vec3_allclose(a, b, rtol=1e-5, atol=1e-8):
#     return (
#         abs(a[0]) <= atol and
#         abs(a[1]) <= atol and
#         abs(a[2] - b[2]) <= atol + rtol * abs(b[2])
#     )

# def vec3_cross(a, b):
#     return array([
#         a[1]*b[2] - a[2]*b[1],
#         a[2]*b[0] - a[0]*b[2],
#         a[0]*b[1] - a[1]*b[0]
#     ])

# def norm3(v):
#     return (v[0]**2 + v[1]**2 + v[2]**2)**0.5

# #-------------------------------------------------------------------------------------

# def rotate_point_to_vector(v, point, opposite=False):
#     v = np.asarray(v, dtype=np.float64)
#     point = np.asarray(point, dtype=np.float64)

#     norm_v = np.linalg.norm(v)
#     if norm_v == 0:
#         return point

#     v = v / norm_v
#     z_axis = np.array([0.0, 0.0, 1.0])

#     if np.allclose(v, z_axis):
#         return point
#     elif np.allclose(v, -z_axis):
#         return -point if not opposite else point

#     # Rotation axis: ẑ × v
#     axis = np.cross(z_axis, v)
#     axis_norm = np.linalg.norm(axis)
#     if axis_norm == 0:
#         return point
#     axis = axis / axis_norm

#     # Angle: arccos(ẑ ⋅ v)
#     angle = np.arccos(v[2])
#     if opposite:
#         angle = -angle

#     # Rodrigues' rotation formula applied directly
#     cos_theta = np.cos(angle)
#     sin_theta = np.sin(angle)
#     k = axis
#     kx, ky, kz = k
#     px, py, pz = point

#     dot_kp = kx*px + ky*py + kz*pz
#     cross = np.cross(k, point)

#     out = (
#         point * cos_theta +
#         cross * sin_theta +
#         k * dot_kp * (1 - cos_theta)
#     )

#     return out

# #-------------------------------------------------------------------------------------

# def triangle_angles_and_area(a, b, c):
#     """
#     Given 3 points in 3D (a, b, c), compute:
#     - internal angles (in degrees)
#     - area using Heron's formula
#     """
#     def length(u, v):
#         return np.linalg.norm(u - v)

#     a = np.asarray(a)
#     b = np.asarray(b)
#     c = np.asarray(c)

#     ab = length(a, b)
#     bc = length(b, c)
#     ca = length(c, a)

#     # Clamp dot products to avoid NaNs due to rounding
#     def safe_angle(u, v):
#         dot_uv = np.dot(u, v)
#         norms = np.linalg.norm(u) * np.linalg.norm(v)
#         return np.arccos(np.clip(dot_uv / norms, -1.0, 1.0))

#     angle_A = safe_angle(b - a, c - a)
#     angle_B = safe_angle(a - b, c - b)
#     angle_C = safe_angle(a - c, b - c)

#     s = 0.5 * (ab + bc + ca)
#     area = max(0.0, (s * (s - ab) * (s - bc) * (s - ca)))**0.5

#     return (
#         np.degrees(angle_A),
#         np.degrees(angle_B),
#         np.degrees(angle_C),
#         area
#     )


# # App UI
# app = dash.Dash(__name__)

# def slider(name, id_, min_=-1, max_=1, step=0.05, val=0.0):
#     return html.Div([
#         html.Label(f"{name}:"),
#         dcc.Slider(id=id_, min=min_, max=max_, step=step, value=val,
#                    marks={-1: "-1", 0: "0", 1: "1"})
#     ], style={"width": "30%", "display": "inline-block", "padding": "10px"})

# app.layout = html.Div([
#     html.H2("Rotate Point to Vector (3D Demo)"),

#     html.Div([
#         slider("Vector X", "vec-x"),
#         slider("Vector Y", "vec-y"),
#         slider("Vector Z", "vec-z", val=1),
#     ]),

#     html.Div([
#         slider("Point X", "point-x", min_=-2, max_=2, val=1),
#         slider("Point Y", "point-y", min_=-2, max_=2, val=1),
#         slider("Point Z", "point-z", min_=-2, max_=2, val=1),
#     ]),

#     html.Div([
#         dcc.Checklist(
#             id="opposite",
#             options=[{"label": "Use Opposite", "value": "yes"}],
#             value=[]
#         )
#     ]),

#     dcc.Graph(id="graph", style={"height": "800px"}),

#     html.Div(id="triangle-info", style={"margin": "20px", "fontFamily": "monospace"})
# ])

# @app.callback(
#     [Output("graph", "figure"), Output("triangle-info", "children")],
#     Input("vec-x", "value"),
#     Input("vec-y", "value"),
#     Input("vec-z", "value"),
#     Input("point-x", "value"),
#     Input("point-y", "value"),
#     Input("point-z", "value"),
#     Input("opposite", "value"),
# )
# def update_graph(vx, vy, vz, px, py, pz, opposite):
#     v = np.array([vx, vy, vz])
#     p = np.array([px, py, pz])
#     rotated = rotate_point_to_vector(v, p, opposite="yes" in opposite)

#     v_norm = v / np.linalg.norm(v) if np.linalg.norm(v) > 0 else v
#     v_draw = v_norm  # Use this for drawing triangle

#     fig = go.Figure()

#     fig.add_trace(go.Scatter3d(
#         x=[0, v[0]],
#         y=[0, v[1]],
#         z=[0, v[2]],
#         mode='lines+markers',
#         marker=dict(size=4),
#         line=dict(width=4),
#         name="Vector v"
#     ))

#     fig.add_trace(go.Scatter3d(
#         x=[p[0]],
#         y=[p[1]],
#         z=[p[2]],
#         mode='markers',
#         marker=dict(size=6, color="red"),
#         name="Original Point"
#     ))

#     fig.add_trace(go.Scatter3d(
#         x=[rotated[0]],
#         y=[rotated[1]],
#         z=[rotated[2]],
#         mode='markers',
#         marker=dict(size=6, color="green"),
#         name="Rotated Point"
#     ))

#     # Coordinate Axes
#     axis_len = 2
#     fig.add_trace(go.Scatter3d(x=[0, axis_len], y=[0, 0], z=[0, 0],
#                             mode="lines", line=dict(color="gray", width=2), name="X Axis"))
#     fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, axis_len], z=[0, 0],
#                             mode="lines", line=dict(color="gray", width=2), name="Y Axis"))
#     fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, axis_len],
#                             mode="lines", line=dict(color="gray", width=2), name="Z Axis"))

#     if "yes" in opposite:
#         # Swap triangle roles when opposite is used
#         # Triangle 1: zhat, rotated point, origin
#         fig.add_trace(go.Mesh3d(
#             x=[0, 0, rotated[0]], y=[0, 0, rotated[1]], z=[0, 1, rotated[2]],
#             i=[0], j=[1], k=[2],
#             opacity=0.3, color='green', name='Rotated Triangle'
#         ))

#         # Triangle 2: v, original point, origin
#         fig.add_trace(go.Mesh3d(
#             x=[0, v_draw[0], p[0]], y=[0, v_draw[1], p[1]], z=[0, v_draw[2], p[2]],
#             i=[0], j=[1], k=[2],
#             opacity=0.3, color='red', name='Original Triangle'
#         ))
#     else:
#         # Triangle 1: zhat, original point, origin
#         fig.add_trace(go.Mesh3d(
#             x=[0, 0, p[0]], y=[0, 0, p[1]], z=[0, 1, p[2]],
#             i=[0], j=[1], k=[2],
#             opacity=0.3, color='red', name='Original Triangle'
#         ))

#         # Triangle 2: v, rotated point, origin
#         fig.add_trace(go.Mesh3d(
#             x=[0, v_draw[0], rotated[0]], y=[0, v_draw[1], rotated[1]], z=[0, v_draw[2], rotated[2]],
#             i=[0], j=[1], k=[2],
#             opacity=0.3, color='green', name='Rotated Triangle'
#         ))

#     if "yes" in opposite:
#         angles1 = triangle_angles_and_area([0, 0, 0], [0, 0, 1], rotated)
#         angles2 = triangle_angles_and_area([0, 0, 0], v_norm, p)
#     else:
#         angles1 = triangle_angles_and_area([0, 0, 0], [0, 0, 1], p)
#         angles2 = triangle_angles_and_area([0, 0, 0], v_norm, rotated)


#     def fmt(angles, label):
#         a1, a2, a3, area = angles
#         return html.Div([
#             html.H4(f"{label}"),
#             html.P(f"Angles: {a1:.2f}°, {a2:.2f}°, {a3:.2f}°"),
#             html.P(f"Area: {area:.4f}")
#         ])

#     info = html.Div([
#         fmt(angles1, "Triangle 1 (Ẑ triangle)"),
#         fmt(angles2, "Triangle 2 (V triangle)")
#     ])

#     # Final layout
#     fig.update_layout(
#         scene=dict(
#             xaxis=dict(range=[-3, 3], backgroundcolor='white', gridcolor='white', zerolinecolor='white'),
#             yaxis=dict(range=[-3, 3], backgroundcolor='white', gridcolor='white', zerolinecolor='white'),
#             zaxis=dict(range=[-3, 3], backgroundcolor='white', gridcolor='white', zerolinecolor='white'),
#             aspectmode='cube',
#         ),
#         margin=dict(l=0, r=0, b=0, t=30),
#         legend=dict(x=0.8, y=0.9)
#     )

#     return fig, info

# if __name__ == "__main__":
#     app.run(debug=True)

# import numpy as np
# from helpers import rotate_point_to_vector, rotate_point_to_vector_ref

# num_trials = 100000
# rtol = 1e-5
# atol = 1e-8

# fail_count = 0
# max_diff = 0.0
# worst_case = None

# for _ in range(num_trials):
#     v = np.random.randn(3)
#     point = np.random.randn(3)

#     out_ref = rotate_point_to_vector_ref(v, point)
#     out_fast = rotate_point_to_vector(v.astype(np.float64), point.astype(np.float64))

#     if not np.allclose(out_ref, out_fast, rtol=rtol, atol=atol):
#         fail_count += 1
#         diff = np.linalg.norm(out_ref - out_fast)
#         if diff > max_diff:
#             max_diff = diff
#             worst_case = (v.copy(), point.copy(), out_ref.copy(), out_fast.copy())

# print(f"\nTotal failures: {fail_count} / {num_trials}")
# print(f"Max Euclidean difference: {max_diff:.3e}")

# if worst_case:
#     v, point, ref, fast = worst_case
#     print("\nWorst case:")
#     print(f"v      = {v}")
#     print(f"point  = {point}")
#     print(f"ref    = {ref}")
#     print(f"fast   = {fast}")
#     print(f"diff   = {ref - fast}")

def four_fun(a,b,c,d):
    return a + (b * c) - d

k = (2,30)
print(four_fun(1,*k,2))