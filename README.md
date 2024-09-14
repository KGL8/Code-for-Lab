# Code-for-Lab

![image](https://github.com/user-attachments/assets/7e9750ba-5e3a-4f1b-88cd-44e73ca45faf)


![Screenshot (12)](https://github.com/user-attachments/assets/5f75df7d-425b-470c-8a52-7559f51601dd)


![image](https://github.com/user-attachments/assets/66d458cb-5a4a-4118-8524-06f32665f8c5)

# <img width="450" alt="Screen Shot 2024-07-09 at 2 22 35 PM" src="https://github.com/KGL8/Code-for-Lab/assets/106930751/834a99da-9932-4783-b96e-92ec0e84ba98">

![spherical_to_distance_plot](https://github.com/KGL8/Code-for-Lab/assets/106930751/df5d926f-db5f-4faa-9f9c-cfe9290aa632)
![histo](https://github.com/KGL8/Code-for-Lab/assets/106930751/0529264e-03c9-48cf-85a2-e7495aa06561)

Current problems:

1. Random Ray Angle Distribution:
   
   In writing the code to select photons of certain energy levels and output their angles through space, I've run into a case that I can't figure out if I like. Firstly, it is clear that, to pick a set of random rays in a range defined by polar angle $\theta$, one cannot simply choose $\theta$ values uniformly. This will result in the following undesired distribution:
   
   <img src="https://github.com/KGL8/Code-for-Lab/assets/106930751/ede21c74-d6c4-4b39-805e-aa83384abc95" width="200" height="200">

   This leads to my case: I am getting a similar distribution, though I can't determine whether it is the fault of the above error or a byproduct of using an exponential ray distribution that favors smaller angles (closer to the center).
