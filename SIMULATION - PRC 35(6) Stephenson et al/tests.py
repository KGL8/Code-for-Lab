# tests.py
from imports import *
from interface import *


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

# γ_E_to_θ_PDF_sv = lambda x: γ_E_to_θ_PDF(x=x,e=E_lvl)
# print(sample_from_pdf(γ_E_to_θ_PDF_sv,*(0,pi/2)).item())