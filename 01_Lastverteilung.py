##
"""
Created on Mon Nov 13 20:10:13 2023

@author: carlos.cruz
"""
import pandas as pd
import numpy as np

header = ['Fy','Fz','Time','MT1','MT2','MQF','FROX','FROY','FROZ','MROX','MROY','MROZ']
df = pd.read_csv('Lasten/Multipurpose_Forces_unverteilt.csv', header=None, names=header)

area = 2714.336/16 # mm2

df['R'] = np.sqrt(df['Fy']**2 + df['Fz']**2) #N
df['Angle_rad'] = np.arctan2(df['Fz'], df['Fy']) #rad
df['Angle_deg'] = np.degrees(df['Angle_rad']) #degree
df['Pressure Hoist_R3'] = df['R']*0.03/area #MPa
df['Pressure Hoist_R17'] = df['R']*0.17/area #MPa
df['Pressure Hoist_R28'] = df['R']*0.28/area #MPa
df['Pressure Hoist_R29'] = df['R']*0.29/area #MPa
df['Pressure Hoist_R19'] = df['R']*0.19/area #MPa
df['Pressure Hoist_R4'] = df['R']*0.04/area #MPa

df.to_csv('Lasten\Multipurpose_verteilt.csv')
