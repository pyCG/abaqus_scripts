# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:33:56 2023

@author: carlos.cruz
"""
from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import optimization
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
from odbAccess import openOdb

directory_path = 'D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model'

odbFilePath = directory_path+'\Job-18.odb'

odb = openOdb(odbFilePath)

lastStep = odb.steps['Step-1']


for i in range(1, 5):

    odb = session.odbs[directory_path+'/Job-18.odb']
    session.writeFieldReport(
        fileName=directory_path+'/Output_U_frame_'+str(i)+'.csv',
        append=OFF, sortItem='Node Label', odb=odb, step=i, frame=6,
        outputPosition=NODAL, variable=(('U', NODAL, ((INVARIANT, 'Magnitude'),
        )), ), stepFrame=SPECIFY)

    odb = session.odbs[directory_path+'/Job-1.odb']
    session.writeFieldReport(
        fileName=directory_path+'/Output_CSTATUS_frame_'+str(i)+'.csv',
        append=OFF, sortItem='Node Label', odb=odb, step=0, frame=i,
        outputPosition=ELEMENT_NODAL, variable=(('CSTATUS', ELEMENT_NODAL), ),
        stepFrame=SPECIFY)

    odb = session.odbs[directory_path+'/Job-1.odb']
    session.writeFieldReport(
        fileName=directory_path+'/Output_CPRESS_frame_'+str(i)+'.csv',
        append=OFF, sortItem='Node Label', odb=odb, step=0, frame=i,
        outputPosition=ELEMENT_NODAL, variable=(('CPRESS', ELEMENT_NODAL), ),
            stepFrame=SPECIFY)

# # Check if arguments are provided
# if len(sys.argv) > 1:
#     number_of_frames = sys.argv[1]
#     directory_path = sys.argv[2]
#     export_data(number_of_frames, directory_path)
# else:
#     print("No arguments provided.")


#%%

from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import optimization
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
from odbAccess import openOdb

directory_path = 'D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model'
odbFilePath = directory_path+'\Job-19.odb'
odb = openOdb(odbFilePath)
number_of_steps = len(odb.steps)
print(number_of_steps)
for i in range(0, number_of_steps):
    session.writeFieldReport(
        fileName=directory_path + '/FE-Scripts/FE-Outputs/Wear_Elements_Contact_Results_Job19_LP_' + str(i+1) + '.csv',
        append=OFF, sortItem='Node Label', odb=odb, step=i, frame=6,
        outputPosition=ELEMENT_NODAL, variable=(
        ('CNORMF', ELEMENT_NODAL), ('CSLIP1', ELEMENT_NODAL), ('CSLIP2', ELEMENT_NODAL), ('CSTATUS', ELEMENT_NODAL)),
        stepFrame=SPECIFY)


    """
    session.writeFieldReport(
             fileName=directory_path+'/Output_Job18_LP_'+str(i+1)+'.csv',
             append=ON, sortItem='Node Label', odb=odb, step=i, frame=6,
             outputPosition=ELEMENT_NODAL, variable=(('CNORMF', ELEMENT_NODAL), ('CSLIP1', ELEMENT_NODAL), ('CSLIP2', ELEMENT_NODAL), ('CSTATUS', ELEMENT_NODAL),
                                                     ('CTANDIR1', ELEMENT_NODAL), ('CTANDIR2', ELEMENT_NODAL), ('COPEN', ELEMENT_NODAL), ('CPRESS', ELEMENT_NODAL),
                                                     ('CSHEAR1', ELEMENT_NODAL), ('CSHEAR2', ELEMENT_NODAL), ('CSHEARF', ELEMENT_NODAL), ('PRESSONLY', ELEMENT_NODAL),
                                                     ('S', ELEMENT_NODAL)),
                 stepFrame=SPECIFY)

""""
        session.writeFieldReport(
             fileName=directory_path+'/Output_Job18_LP_'+str(i)+'.csv',
             append=OFF, sortItem='Node Label', odb=odb, step=i, frame=6,
             outputPosition=ELEMENT_NODAL, variable=(('CNORMF', ELEMENT_NODAL), ('CSLIP1', ELEMENT_NODAL), ('CSLIP2', ELEMENT_NODAL), ('CSTATUS', ELEMENT_NODAL)),
                 stepFrame=SPECIFY)
