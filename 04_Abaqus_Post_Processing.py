##
import pandas as pd
import numpy as np
import warnings
from cg_Wear_Archard_Fleischer_Plot import ARCHARD_wear_model
from cg_Wear_Archard_Fleischer_Plot import FLEISCHER_wear_model
from cg_Wear_Archard_Fleischer_Plot import plot_node_values

# Turn off all Python warnings
warnings.filterwarnings("ignore")
# %%

# =============================================================================
# Function Activation
# =============================================================================
# %%
execute_export_abaqus_output = False
execute_stress_disp_contact_plot = True
execute_plot_archard_wear = True
execute_plot_fleischer_wear = True

directory_path = 'RescueHoist'
last_frame = 1001  # Set this to the last frame number
k = 0.0001
H = 120
mu = 0.2
e_R = 100000
# =============================================================================
# PARAMETERS
# =============================================================================

for i in range(1, last_frame):
    print(f'-- Load Step: {i}')
    # import current Contact_Results_Job19 file
    df_current_step = pd.read_csv(f'{directory_path}/RescueHoist_Abaqus_Job19_LP_{i}_Full_Ring.csv')
    # remove spaces from the header
    df_current_step.columns = df_current_step.columns.str.lstrip()
    # convert string to float for the CSLIP variable
    df_current_step['CSLIP1'] = df_current_step['CSLIP1'].astype(float)
    df_current_step['CSLIP2'] = df_current_step['CSLIP2'].astype(float)
    # remove space for the CSTATUS content "NoValue"
    df_current_step['CSTATUS'] = df_current_step['CSTATUS'].str.lstrip()
    # Set "NoValue" = 0, it means that a contact is not stablished
    df_current_step.loc[df_current_step['CSTATUS'] == 'NoValue', 'CSTATUS'] = 0
    # convert string to float for the CSTATUS variable
    df_current_step['CSTATUS'] = df_current_step['CSTATUS'].astype(float)
    # define sticking and sliping as contact stablished
    df_current_step.loc[df_current_step['CSTATUS'] == 2, 'CSTATUS'] = 1
    # calculate absolute relative displacement CSLIP
    df_current_step['CSLIP'] = (df_current_step['CSLIP1'])

    if i == 1:
        df_current_step['DELTA_CSLIP'] = df_current_step['CSLIP']
        df_current_step['DELTA_CNORMF-Magnitude'] = df_current_step['CNORMF-Magnitude'] / 2

        df_current_step['Archard-Wear'] = ARCHARD_wear_model(p_A=df_current_step['DELTA_CNORMF-Magnitude'],
                                                             s=df_current_step['DELTA_CSLIP'],
                                                             k=k,
                                                             H=H)

        df_current_step['Fleischer-Wear'] = FLEISCHER_wear_model(p_A=df_current_step['DELTA_CNORMF-Magnitude'],
                                                                 s=df_current_step['DELTA_CSLIP'],
                                                                 mu=mu,
                                                                 e_R=e_R)

        df_current_step['Cumulative-Archard-Wear'] = df_current_step['Archard-Wear']
        df_current_step['Cumulative-Fleischer-Wear'] = df_current_step['Fleischer-Wear']
        df_current_step.to_csv(f'{directory_path}/RescueHoist_Wear_Job19_LP_{i}_Full_Ring.csv', index=False)

    else:
        df_previous_step = pd.read_csv(f'{directory_path}/RescueHoist_Wear_Job19_LP_{i-1}_Full_Ring.csv')
        df_current_step['DELTA_CSLIP'] = df_current_step['CSLIP'] - df_previous_step['CSLIP']
        df_current_step['DELTA_CNORMF-Magnitude'] = (df_current_step['CNORMF-Magnitude'] + df_previous_step['CNORMF-Magnitude']) / 2

        df_current_step['Archard-Wear'] = ARCHARD_wear_model(p_A=df_current_step['DELTA_CNORMF-Magnitude'],
                                                             s=df_current_step['DELTA_CSLIP'],
                                                             k=k,
                                                             H=H)

        df_current_step['Fleischer-Wear'] = FLEISCHER_wear_model(p_A=df_current_step['DELTA_CNORMF-Magnitude'],
                                                                 s=df_current_step['DELTA_CSLIP'],
                                                                 mu=mu,
                                                                 e_R=e_R)

        df_current_step['Cumulative-Archard-Wear'] = df_previous_step['Cumulative-Archard-Wear'] + df_current_step['Archard-Wear']
        df_current_step['Cumulative-Fleischer-Wear'] = df_previous_step['Cumulative-Fleischer-Wear'] + df_current_step['Fleischer-Wear']
        df_current_step.to_csv(f'{directory_path}/RescueHoist_Wear_Job19_LP_{i}_Full_Ring.csv', index=False)

    if i == last_frame - 1:

        x = df_current_step['X']
        y = df_current_step['Y']
        z = df_current_step['Z']

        if execute_stress_disp_contact_plot == True:
            titles = ['CNORMF-Magnitude', 'CSLIP', 'Cumulative-Fleischer-Wear', 'Cumulative-Archard-Wear']

            for title in titles:
                plot_node_values(w=df_current_step[title],
                                 x=z,
                                 y=y,
                                 z=x,
                                 title=title,
                                 save_path='PlotResults',
                                 file_name='RescueHoist',
                                 show_plot=True)

##
