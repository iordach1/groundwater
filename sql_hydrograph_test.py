# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyodbc
import pandas as pd

#connect to sql db
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=SWSDATASTORM;DATABASE=groundwaterproddatabase;UID=gw_ob_web_user;PWD=dfuU^SDu3ddd')

#sql statement to select pertinent data
#!-- fix to pull location data also
sql = """
SELECT 
    measure.TIMESTAMP AS TIMESTAMP, 
    measure.P_Number AS P_Number, 
    measure.DTW_FT_RAW AS DTW_FT_RAW, 
    measure.DTW_FT_Reviewed AS DTW_FT_Reviewed, 
    measure.Water_Surface_Elevation AS Water_Surface_Elevation, 
    info.WELL_NAME AS Well_Name,
    info.WELL_NAME_ALT AS Well_Name_Alt,
    info.NETWORK_1 AS Network,
    info.LOCAL_AQ_NAME as Aquifer
FROM 
    [groundwaterproddatabase].[GW_OBV].[OB_MEASUREMENTS] AS measure
    INNER JOIN [groundwaterproddatabase].[GW_OBV].[OB_WELLS] AS info ON measure.P_Number = info.P_NUMBER and measure.P_Number IN {0}
ORDER BY 
    P_Number ASC, 
    TIMESTAMP ASC
""".format(                 #p_numbers of interest... not including Illinois American
                (   
                    381643,
                    381644,
                    381645,
                    381646,
                    381651,
                    381652,
                    381653,
                    381654,
                    381676,
                    65886,
                    170846,
                    171107,
                    236005,
                    236006,
                    236009,
                    286731,
                    294641,
                    360669,
                    360672,
                    360673,
                    360677,
                    491517,
                    492891,
                    494517,
                    492891,
                    494075,
                    498300,
                    498310
                )
            )

test_df = pd.read_sql(sql, conn)    #read data into df
conn.close()    #close the server connection

test_df['TIMESTAMP'] = pd.to_datetime(test_df['TIMESTAMP'], infer_datetime_format=True) #convert timestamps to dt format

unique_pnum = test_df.P_Number.unique()
unique_name = test_df.Well_Name.unique()

# generate plots
for i in range(0, len(unique_pnum)):
    plt = test_df[test_df['P_Number'] == unique_pnum[i]].plot(
                                            x = 'TIMESTAMP',
                                            y = 'Water_Surface_Elevation',
                                            title = str(unique_name[i]),
                                            figsize=(11, 8.5)
                                            ).get_figure()
    plt.savefig("{0}_{1}.jpg".format(unique_pnum[i], unique_name[i]))