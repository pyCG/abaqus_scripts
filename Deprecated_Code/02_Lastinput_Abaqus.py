'''
import csv
def select_column(csv_file, column_name):
        with open(csv_file, 'r') as file:
            return [float(row[column_name]) for row in csv.DictReader(file)]

file_path = 'D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model\FE-Scripts\FE-Inputs\Rescue_Hoist_verteilt.csv'


kraft_name = ['Rescue_Hoist_R3', 'Rescue_Hoist_R4', 'Rescue_Hoist_R17', 'Rescue_Hoist_R19', 'Rescue_Hoist_R28', 'Rescue_Hoist_R29']
time_steps = list(range(1000))

for i in range(0, len(kraft_name)):
    load_points = select_column(file_path, kraft_name[i])
    print(load_points)
    #load_spectrum = list(zip(time_steps, load_points))
    #mdb.models['Model-12'].amplitudes[kraft_name[i]].setValues(data=load_spectrum, smooth=SOLVER_DEFAULT, timeSpan=STEP)


#%%
'''
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

csv_file_path = r'/Lasten/Multipurpose_verteilt.csv'
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

#%%


## Create the Steps
'''   
for i in range(1, 1000):
    mdb.models['Model-13'].StaticStep(initialInc=0.0001, minInc=1e-15, name='Step-'+str(i+1), previous='Step-'+str(i))
 
for i in range(1, 1001):
    mdb.models['Model-14'].steps['Step-'+str(i)].setValues(adaptiveDampingRatio=0.05, continueDampingFactors=False, stabilizationMagnitude=0.0002, stabilizationMethod=DISSIPATED_ENERGY_FRACTION)

'''




# mdb.models['Model-18'].StaticStep(adaptiveDampingRatio=None, 
# continueDampingFactors=False, initialInc=0.1, minInc=1e-15, name='Step-'+str(i+1), 
#     previous='Step-'+str(i), stabilizationMagnitude=0.0002, stabilizationMethod=
#     DISSIPATED_ENERGY_FRACTION)