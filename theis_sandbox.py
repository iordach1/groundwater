# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 18:30:55 2019

barebones script that calculates theis equation in 2d for 3 randomly placed wells

plots drawdown contours for 5 timesteps

units are arbitrary lets assume meters and days for simplicity

TODO:
    more interactivity to change parameters [gui perhaps]
    scaling factor to translate grid to real-world units
    create hydrographs for "monitoring wells"
    recharge?

@author: viord
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import exp1 #exponential integral

def get_u(r, S, T, t):  return r**2*S/4/T/t #dimensionless time parameter

def drawdown(t, S, T, Q, r):    
    return Q/2/np.pi/T*exp1(get_u(r, S, T, t)) #calculate drawdown at given point for given time

def distance_from_well (point, well_1): #calculate distance from well at given point
    return np.linalg.norm(point-well_1)
    

Q,S,T = -1500, 0.00025, 250  #pumping rate, storage coefficient, transmissivity
t = np.array([100,500,1000,5000,10000]) #time steps

#grid dimensions 4096x4096 [>16 million nodes] is approaching the limit for what most modern
#cpu's RAM can handle... may even be overkill depending on the resolution necessary
dim_x = np.uint16(2**12)
dim_y = np.uint16(2**12)

#using meshgrids saves on computation time
xv, yv = np.meshgrid(np.arange(dim_x), np.arange(dim_y), sparse = True)

#generate 3 random wells
well_1 = np.array([np.random.randint(0, dim_x), np.random.randint(0, dim_y)], dtype = 'uint16')
well_2 = np.array([np.random.randint(0, dim_x), np.random.randint(0, dim_y)], dtype = 'uint16')
well_3 = np.array([np.random.randint(0, dim_x), np.random.randint(0, dim_y)], dtype = 'uint16')

#calsulate distance to wells from each point on the grid
dist_1 = distance_from_well(np.array([xv,yv]), well_1)
dist_2 = distance_from_well(np.array([xv,yv]), well_2)
dist_3 = distance_from_well(np.array([xv,yv]), well_3)
    
#calculate drawdown surfaces for each well independently, combine surfaces, contour
#change Q in first 2 wells... for funsies
for time in t:
    theis_drawdown_1 = drawdown(time,S,T,Q-500,dist_1)
    theis_drawdown_2 = drawdown(time,S,T,Q+500,dist_2)
    theis_drawdown_3 = drawdown(time,S,T,Q,dist_3)
    theis_drawdown = theis_drawdown_1 + theis_drawdown_2 + theis_drawdown_3
    fig = plt.figure(figsize = (15, 15))
    ax = fig.add_subplot(111)
    #cpf = ax.contourf(theis_drawdown, 5, cmap ='seismic')
    cp = ax.contour(theis_drawdown, levels = np.arange(-55,0,5), colors = 'k')
    ax.scatter([well_1[0],well_2[0],well_3[0]],[well_1[1],well_2[1],well_3[1]], marker ='+', c = 'lightblue', s = 25, linewidth = 25)
    ax.scatter([well_1[0],well_2[0],well_3[0]],[well_1[1],well_2[1],well_3[1]], marker ='o', s = 10, c= 'lightblue', linewidth = 10)
    ax.text(well_1[0]+50,well_1[1]-120,'well-1\nQ={0}'.format(Q-500))
    ax.text(well_2[0]+50,well_2[1]-120,'well-2\nQ={0}'.format(Q+500))
    ax.text(well_3[0]+50,well_3[1]-120,'well-3\nQ={0}'.format(Q))
    ax.clabel(cp, fontsize = 12, colors = 'k')
    ax.set_title("t = {0}, S = {1}, T = {2}".format(time, S, T))
    plt.show()
