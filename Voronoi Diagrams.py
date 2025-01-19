# BY DANIEL ARANDA, JIMENA CAMPOS AND HANCEL BORREGO
import numpy as np
import scipy
from matplotlib import colors
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d, SphericalVoronoi
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------


npoints = 100 # number of points   

# For the creation of N points on the unit sphere

# Random points
def n_random_sphere_points(npoints):
    list_of_points = []
    angle_phi = np.pi * np.random.rand(npoints)
    angle_theta = 2 * np.pi * np.random.rand(npoints)
    for i in range(npoints):
        provisional = []
        provisional.append(np.sin(angle_phi[i]) * np.cos(angle_theta[i]))
        provisional.append(np.sin(angle_phi[i]) * np.sin(angle_theta[i]))
        provisional.append(np.cos(angle_phi[i]))
        list_of_points.append(provisional)
    return np.array(list_of_points)

# Using a Fibonacci sequence
def fibonacci_sphere_points(npoints):
    goldenRatio = (1 + 5**0.5)/2
    i = np.arange(0, npoints)
    theta = 2 * np.pi * i / goldenRatio
    phi = np.arccos(1 - 2*(i)/npoints)
    x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi);

    list_of_points = [[x[i],y[i],z[i]] for i in range(npoints)]
    return np.array(list_of_points)

# Created manually, gives color to each polygon based on number of sides
color_code = { 
    3: [0.733, 0.941, 0.494],
    4: [0.898, 0.941, 0.494], 
    5: [0.941, 0.749, 0.494],
    6: [0.922, 0.318 , 0.878],
    7: [0.922, 0.659, 0.878],
    8: [0.58, 0.878, 0.878],
    9: [0.58, 0.886, 1, 0.878], 
    10: [0.161, 0.267, 0.98, 0.878], 
    11: [0.694, 0.161, 0.98, 0.878],
    12: [0.98, 0.161, 0.91, 0.878],
    13: [0.98, 0.161, 0.259, 0.878],
    14: 'r' ,
    15: 'm' }


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------


points = fibonacci_sphere_points(npoints) # The one below can be used too
#points = n_random_sphere_points(npoints)

# Creating the regions using SphericalVoronoi in Scipy
sv = SphericalVoronoi(points) 
sv.sort_vertices_of_regions()

# Doing the special sum
sum = 0
for region in sv.regions: #sv.regions is a list of lists, the nth list contains the indices of the vertices corresponding to the nth point
    s = len(region) #since number of sides = number of vertices, i just need how many vertices there are per polygon
    sum += 6 - s 

print("The sum is: ",sum)


#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#This plots the vertices and generating points, the numbers are related to the coord (from 0 to 2, cause there are 3 dimensions)

ax.scatter(sv.vertices[:,0], sv.vertices[:,1], sv.vertices[:,2], color='r') # Vertices of the polygons in - RED -
ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b') # Starting points (on the sphere) in - BLUE -


for n in range(0, len(sv.regions)): #this is range(number of polygons) 
    region = sv.regions[n] #see description for sum
    polygon = Poly3DCollection([sv.vertices[region]], alpha=1.0)
    ''' For the line above: alpha is the opacity, sv.vertices has all vertices as points (double array), region is a list, being in the argument 
    makes it take the corresponding indexed vertices, outer [] in first argument is due to the format for the function '''
    polygon.set_color(color_code[len(region)])
    ax.add_collection3d(polygon)


#This changes the point of view
ax.azim = 10
ax.elev = 40


#This hides the axis

_ = ax.set_xticks([])

_ = ax.set_yticks([])

_ = ax.set_zticks([])


fig.set_size_inches(8, 8)

plt.show()