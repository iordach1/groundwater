# -*- coding: utf-8 -*-
#What manner of man are you that can summon up fire without flint or tinder?
import os, conda; os.environ['PROJ_LIB'] = os.path.join(conda.__file__.split('lib')[0], r'pkgs\proj4-5.2.0-ha925a31_1\Library\share'); del os
shapefile = open(conda.__file__.split(r'\conda')[0] + r'\shapefile.py','r');replace = shapefile.read().replace("utf-8","latin-1");shapefile.close()
shapefile = open(conda.__file__.split(r'\conda')[0] + r'\shapefile.py','w');shapefile.write(replace);shapefile.close(); del conda, shapefile
#I... am an enchanter. ... There are some who call me... 'Tim'?

r"""
Created on Tue Jul  2 14:57:46 2019

Test script to get basemap working in spyder.
@author: iordach1

Notes:
    
    -->    in anaconda prompt run the following command to completion:
                conda install basemap basemap-data-hires
        
    -->    to get the bleeding edge [read 'potentially unstable'] release:
                conda install -c conda-forge basemap basemap-data-hires
        
                *be careful exploring the conda-forge... do not delve too greedily nor too deep
    
    -->    run this script a first time
                the first time you run it, the drawcounties() function won't work properly and the script will fail
                don't panic!
    
    -->    run this script a second time
                voila!... if all went well you should have a pretty map of the greatest state in the Union
                basemap should work now for all future scripts
"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#--
mp = Basemap(
        projection = 'lcc',
        lat_0 = 39.73,
        lon_0 = -89.5,
        width = 350000,
        height = 625000,
        resolution='h'
        )

mp.drawcounties()
mp.etopo()
mp.drawcoastlines(linewidth=1.5)
mp.drawrivers(color='cyan', linewidth=1.25)
mp.drawstates(zorder=20, linewidth=1.5)
mp.drawmapscale(-90.75, 37.5, -90.75, 37.5, 100, barstyle='fancy', zorder = 100, fontsize=10)

plt.title('Map of Illinois', fontsize=16)
fig = plt.gcf()
fig.set_size_inches((8.5, 11))
plt.show()
fig.savefig('map_ill.png', dpi=100)
#--