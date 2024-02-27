import csv
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

csv_file_path = r'C:\Users\carlos.cruz\PycharmProjects\abaqus_scripts\Lasten\Multipurpose_verteilt.csv'
i = 0
model = 'Model-20'
with open(csv_file_path, 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if i > 0:
            # print(row)
            print(i)
            # print(row[16])
            # print(row[17])
            # print(row[18])
            # print(row[19])
            # print(row[20])
            # print(row[21])
            print('===========================================')
            mdb.models[model].loads['Kraft1-WK10-P3'].setValuesInStep(magnitude=float(row[16]), stepName='Step-'+str(i))
            mdb.models[model].loads['Kraft1-WK11-P17'].setValuesInStep(magnitude=float(row[17]), stepName='Step-'+str(i))
            mdb.models[model].loads['Kraft1-WK12-P28'].setValuesInStep(magnitude=float(row[18]), stepName='Step-'+str(i))
            mdb.models[model].loads['Kraft1-WK13-P29'].setValuesInStep(magnitude=float(row[19]), stepName='Step-'+str(i))
            mdb.models[model].loads['Kraft1-WK14-P19'].setValuesInStep(magnitude=float(row[20]), stepName='Step-'+str(i))
            mdb.models[model].loads['Kraft1-WK15-P4'].setValuesInStep(magnitude=float(row[21]), stepName='Step-'+str(i))
        i = i+1