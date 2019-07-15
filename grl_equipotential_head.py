# -*- coding: utf-8 -*-
import os, conda; os.environ['PROJ_LIB'] = os.path.join(conda.__file__.split('lib')[0], r'pkgs\proj4-5.2.0-ha925a31_1\Library\share'); del os
shapefile = open(conda.__file__.split(r'\conda')[0] + r'\shapefile.py','r');replace = shapefile.read().replace("utf-8","latin-1");shapefile.close()
shapefile = open(conda.__file__.split(r'\conda')[0] + r'\shapefile.py','w');shapefile.write(replace);shapefile.close(); del conda, shapefile

"""
Created on Fri Jul 12 10:23:01 2019

@author: iordach1
"""


import pyodbc
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
#import matplotlib.pyplot as plt

#connect to sql db
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SWSDATASTORM;DATABASE=groundwaterproddatabase;UID=GWDATAREADER;PWD=ModusLatin1')

wells = (
            381639,
            381640,
            381641,
            381642,
            381643,
            381644,
            381645,
            381646,
            381647,
            381648,
            381649,
            381650,
            381651,
            381652,
            381653,
            381654,
            381655,
            381656,
            381657,
            381658,
            381659,
            381660,
            381661,
            381662,
            381663,
            381664,
            381665,
            381666,
            381668,
            381669,
            381670,
            381671,
            381672,
            381673,
            381674,
            381675,
            381676,
            381677,
            381678
        )

basicINFO_sql = """
SELECT
    location.P_NUMBER as P_NUMBER,
    info.WELL_NAME as WELL_NAME,
    location.X_LAMBERT as X_LAMBERT,
    location.Y_LAMBERT as Y_LAMBERT,
    location.LONG_WGS_84 as LONG_WGS_84,
    location.LAT_WGS_84 as LAT_WGS_84,
    info.LOCAL_AQ_NAME as LOCAL_AQ_NAME
FROM
    [groundwaterproddatabase].[GW_OBV].[OB_LOCATIONS] as location
    INNER JOIN [groundwaterproddatabase].[GW_OBV].[OB_WELLS] AS info 
        ON location.P_NUMBER = info.P_NUMBER 
            AND location.P_Number IN {0}
ORDER BY
    P_NUMBER ASC
""".format(wells)

basic_info_df = pd.read_sql(sql = basicINFO_sql, con = conn, index_col = 'P_NUMBER')

telemetryWaterLevel_sql = """
SELECT
    measure.P_Number AS P_NUMBER, 
    measure.TIMESTAMP AS TIMESTAMP,  
    measure.DTW_FT_RAW AS DTW_FT_RAW, 
    measure.DTW_FT_Reviewed AS DTW_FT_Reviewed, 
    measure.Water_Surface_Elevation AS Water_Surface_Elevation
FROM 
    [groundwaterproddatabase].[GW_OBV].[OB_MEASUREMENTS] AS measure
WHERE
    P_NUMBER IN {0}
ORDER BY 
    P_NUMBER ASC, 
    TIMESTAMP ASC
""".format(wells)

telemetry_water_level_df = pd.read_sql(sql = telemetryWaterLevel_sql, con = conn)
telemetry_water_level_df['source'] = 'TELEMETRY'

handWaterLevel_sql= """
SELECT
    measure.p_num AS P_NUMBER, 
    measure.meas_date AS DATE,
    measure.meas_time AS TIME,
    measure.meas_depth AS DTW_FT_RAW,
    measure.meas_depth AS DTW_FT_Reviewed,
    measure.mp_elevation - measure.meas_depth as Water_Surface_Elevation
FROM
    [groundwaterproddatabase].[dbo].[gw_water_level_measurements] as measure
WHERE
    p_num IN {0}
ORDER BY
    P_NUMBER ASC,
    DATE ASC,
    TIME ASC
""".format(wells)

hand_water_level_df = pd.read_sql(sql = handWaterLevel_sql, con = conn)

hand_water_level_df['DATE'] = pd.to_datetime(hand_water_level_df['DATE'], infer_datetime_format = True)
hand_water_level_df['DATE'] = hand_water_level_df['DATE'].apply(lambda x: x.date())

hand_water_level_df['TIME'] = pd.to_datetime(hand_water_level_df['TIME'], infer_datetime_format = True)
hand_water_level_df['TIME'] = hand_water_level_df['TIME'].fillna(pd.to_datetime('00:00:00'))
hand_water_level_df['TIME'] = hand_water_level_df['TIME'].apply(lambda x: x.time())

hand_water_level_df['TIMESTAMP'] = pd.to_datetime(hand_water_level_df['DATE'].astype(str) + ' ' + hand_water_level_df['TIME'].astype(str))

hand_water_level_df['source'] = 'HAND MEASUREMENT'

hand_water_level_df = hand_water_level_df[['P_NUMBER', 'TIMESTAMP', 'DTW_FT_RAW', 'DTW_FT_Reviewed', 'Water_Surface_Elevation', 'source']]

conn.close()

water_level_df = telemetry_water_level_df.append(hand_water_level_df).sort_values(by=['P_NUMBER', 'TIMESTAMP'])

unique_pnum = water_level_df['P_NUMBER'].unique()

# for i in range(0, len(unique_pnum)):
#     plt = water_level_df[water_level_df['P_NUMBER'] == unique_pnum[i]].plot(
#                                             x = 'TIMESTAMP',
#                                             y = 'Water_Surface_Elevation',
#                                             style = ':',
#                                             marker = 'o',
#                                             title = str(basic_info_df['WELL_NAME'][unique_pnum[i]]) + ' -- ' + str(basic_info_df['LOCAL_AQ_NAME'][unique_pnum[i]]),
#                                             figsize=(11, 8.5)
#                                             ).get_figure()
#     plt.savefig("{0}_{1}.jpg".format(unique_pnum[i], basic_info_df['WELL_NAME'][unique_pnum[i]]))

basic_info_df.to_csv('basic_info.csv')
water_level_df.to_csv('water_level.csv')