##
import pandas as pd


directory_folder = 'RescueHoist'

list_max_wear_archard = []
list_max_wear_fleischer = []
list_relative_displacement = []
list_normal_force = []

number_load_steps = 1001

df = pd.read_csv(f'{directory_folder}\RescueHoist_Wear_Job19_LP_1000.csv')
max_value_fleischer = df['Cumulative-Fleischer-Wear'].max()
index_of_max_value = df[df['Cumulative-Fleischer-Wear'] == max_value_fleischer].index[0]

for i in range(1, number_load_steps):

    df = pd.read_csv(f'{directory_folder}\RescueHoist_Wear_Job19_LP_{i}.csv')
    max_value_fleischer = df['Fleischer-Wear'].iloc[index_of_max_value]
    max_value_archard = df['Archard-Wear'].iloc[index_of_max_value]

    list_max_wear_archard.append(max_value_fleischer)
    list_max_wear_fleischer.append(max_value_archard)

    list_relative_displacement.append(df.at[index_of_max_value, 'DELTA_CSLIP'])
    list_normal_force.append(df.at[index_of_max_value, 'DELTA_CNORMF-Magnitude'])

df_rescue_hoist = pd.read_csv('Lasten/Rescue_Hoist_verteilt.csv')

df_rescue_hoist['DELTA_CSLIP'] = list_relative_displacement
df_rescue_hoist['DELTA_CNORMF_Magnitude'] = list_normal_force

df_rescue_hoist['Baseline Max Archard Wear'] = list_max_wear_archard
df_rescue_hoist['Baseline Max Fleischer Wear'] = list_max_wear_fleischer
df_rescue_hoist['Baseline Cumulative Max Archard Wear'] = df_rescue_hoist['Baseline Max Archard Wear'].cumsum()
df_rescue_hoist['Baseline Cumulative Max Fleischer Wear'] = df_rescue_hoist['Baseline Max Fleischer Wear'].cumsum()

df_rescue_hoist.to_csv('Baseline/RescueHoist_Baseline.csv', index=False)
df_rescue_hoist.to_excel('Baseline/RescueHoist_Baseline.xlsx', index=False)


##

