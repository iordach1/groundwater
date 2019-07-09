# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:53:07 2019

script converts raw dat files into format specified by Erin Bauer

@author: iordach1
"""
import pandas as pd

#input and output paths
input_dir = r"\\swsredbird\LoggerNet"'\\'
input_files = [
            "San Jose_Belfort",             #12_Belfort
            "Tree Nursery MTOW-06_Belfort"  #9_Belfort
            ]
output_dir = 'converted_rainGauge''\\'

alt_file_name = {
        "San Jose_Belfort":"12_Belfort",
        "Tree Nursery MTOW-06_Belfort":"9_Belfort"
        }

for file in input_files:
    #read in raw .dat files
    dataframe = pd.read_csv(
            filepath_or_buffer = "{0}{1}.dat".format(input_dir, file),
            skiprows = [0,2,3],
            parse_dates = ['TIMESTAMP'],
            infer_datetime_format = True
            )

    #convert to specified format
    dataframe['#'] = dataframe['RECORD'] + 1
    dataframe['MN'] = dataframe['TIMESTAMP'].dt.month
    dataframe['DT'] = dataframe['TIMESTAMP'].dt.day
    dataframe['YR'] = dataframe['TIMESTAMP'].dt.year
    dataframe['YR'] = dataframe['YR'] % 1000
    dataframe['Hour'] = dataframe['TIMESTAMP'].dt.hour
    dataframe['Minute'] = dataframe['TIMESTAMP'].dt.minute
    dataframe['Second'] = dataframe['TIMESTAMP'].dt.second
    dataframe['Inches'] = dataframe['Primary']
    dataframe['Batt (V)'] = 3

    #ah, FORTRAN... pad numbers with leading 0's
    dataframe['MN'] = dataframe['MN'].apply(lambda x: '{0:0>2}'.format(x))
    dataframe['DT'] = dataframe['DT'].apply(lambda x: '{0:0>2}'.format(x))
    dataframe['Hour'] = dataframe['Hour'].apply(lambda x: '{0:0>2}'.format(x))
    dataframe['Minute'] = dataframe['Minute'].apply(lambda x: '{0:0>2}'.format(x))
    dataframe['Second'] = dataframe['Second'].apply(lambda x: '{0:0>2}'.format(x))

    #drop raw columns
    dataframe.drop(columns = ['TIMESTAMP', 'RECORD', 'Primary', 'Primary_Avg'], inplace = True)

    #output data
    dataframe.to_csv(
                path_or_buf = "{0}{1}{2}.csv".format(input_dir, output_dir, alt_file_name[file]),
                index = False
                )

    #add the plot title line
    with open("{0}{1}{2}.csv".format(input_dir, output_dir, alt_file_name[file]), "r") as infile:
        reader = infile.read()
        reader = "Plot Title: from {0},\n".format(alt_file_name[file]) + reader

    infile.close()

    with open("{0}{1}{2}.csv".format(input_dir, output_dir, alt_file_name[file]), "w") as outfile:

        for line in reader:
            outfile.write(line)

    outfile.close()