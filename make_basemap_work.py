# -*- coding: utf-8 -*-
#What manner of man are you that can summon up fire without flint or tinder?
import os, conda; os.environ['PROJ_LIB'] = os.path.join(conda.__file__.split('lib')[0], r'pkgs\proj4-5.2.0-ha925a31_1\Library\share'); del os, conda
#I... am an enchanter. ... There are some who call me... 'Tim'?

r"""
Created on Tue Jul  2 14:57:46 2019

Test script to get basemap working in spyder.
@author: iordach1

Notes:
    
    -->    in anaconda prompt run the following command to completion:
                conda install basemap basemap-data-hires
        
    -->    if you find that basemap still doesn't work try the following:
                conda install -c conda-forge basemap basemap-data-hires
        
                *be careful exploring the conda-forge... do not delve too greedily nor too deep 
     
    -->    include line 3 of this script [above] in any other script that utilizes basemap
    
    -->    in order to get drawcounties() to work:
                open C:\users\[YOUR USERNAME HERE]\AppData\Local\Continuum\anaconda3\lib\site-packages\shapefile.py
                replace all references to 'utf-8' to 'latin-1'
                will this mess up a gis-centric script you run in the future?... probably
    
    -->    run this script
                if all went well, you should end up with a pretty map of the best state in the Union
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

mp.etopo()
mp.drawcoastlines(linewidth=1.5)
mp.drawrivers(color='cyan', linewidth=1.25)
mp.drawstates(zorder=20, linewidth=1.5)
mp.drawcounties()
mp.drawmapscale(-90.75, 37.5, -90.75, 37.5, 100, barstyle='fancy', zorder = 100, fontsize=10)

plt.title('Map of Illinois', fontsize=16)
fig = plt.gcf()
fig.set_size_inches((8.5, 11))
plt.show()
fig.savefig('map_ill.png', dpi=100)
#--