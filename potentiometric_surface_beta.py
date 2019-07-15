# -*- coding: utf-8 -*-
#What manner of man are you that can summon up fire without flint or tinder?
import os, conda; os.environ['PROJ_LIB'] = os.path.join(conda.__file__.split('lib')[0], r'pkgs\proj4-5.2.0-ha925a31_1\Library\share'); del os
shapefile = open(conda.__file__.split(r'\conda')[0] + r'\shapefile.py','r');replace = shapefile.read().replace("utf-8","latin-1");shapefile.close()
shapefile = open(conda.__file__.split(r'\conda')[0] + r'\shapefile.py','w');shapefile.write(replace);shapefile.close(); del conda, shapefile
#I... am an enchanter. ... There are some who call me... 'Tim'?

"""
Created on Sat Jul 13 22:44:56 2019

@author: viord
"""

import pandas as pd
import numpy as np

#from mpl_toolkits.basemap import Basemap
from pykrige.ok import OrdinaryKriging
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def select_water_levels(df, year, condition):
    df = df[(df['TIMESTAMP']>=pd.Timestamp(year = year, month = 1, day = 1)) & (df['TIMESTAMP']<=pd.Timestamp(year = year, month = 12, day = 31))]
    
    if condition == 'min':
        df = df.sort_values('Water_Surface_Elevation', ascending=True).drop_duplicates(['P_NUMBER'])
    else:   df = df.sort_values('Water_Surface_Elevation', ascending=False).drop_duplicates(['P_NUMBER'])
    
    return df

basic_info = pd.read_csv('basic_info.csv', index_col = 'P_NUMBER')
water_level = pd.read_csv('water_level.csv', parse_dates = ['TIMESTAMP'], low_memory = False, engine = 'c')
#water_level['TIMESTAMP'] = pd.to_datetime(water_level['TIMESTAMP'])

basic_info = basic_info[basic_info['LOCAL_AQ_NAME'] == 'SANKOTY']

water_level = water_level[water_level['P_NUMBER'].isin(basic_info.index)]

#1991 min
min_1991 = select_water_levels(water_level, 1991, 'min')
#1991 max
max_1991 = select_water_levels(water_level, 1991, 'max')
#2012 min
min_2012 = select_water_levels(water_level, 2012, 'min')
#2012 max
max_2012 = select_water_levels(water_level, 2012, 'max')
#2018 min
min_2018 = select_water_levels(water_level, 2018, 'min')
#2018 max
max_2018 = select_water_levels(water_level, 2018, 'max')
#2019 max
max_2019 = select_water_levels(water_level, 2019, 'max')