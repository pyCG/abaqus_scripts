##
import pandas as pd



directory_folder = 'RescueHoist'

list_max_wear_archard = []
list_max_wear_fleischer = []
list_relative_displacement = []
list_normal_force = []
list_load_duration = []
list_load_change = []
number_load_steps = 1001

df = pd.read_csv(f'{directory_folder}\RescueHoist_Wear_Job19_LP_1000.csv')
max_value_fleischer = df['Cumulative-Fleischer-Wear'].max()
index_of_max_value = df[df['Cumulative-Fleischer-Wear'] == max_value_fleischer].index[0]

for i in range(1, number_load_steps):

    df = pd.read_csv(f'{directory_folder}\RescueHoist_Wear_Job19_LP_{i}.csv')
    max_value_fleischer = df['Fleischer-Wear'].iloc[index_of_max_value]
    max_value_archard = df['Archard-Wear'].iloc[index_of_max_value]

    list_max_wear_archard.append(max_value_archard)
    list_max_wear_fleischer.append(max_value_fleischer)

    list_relative_displacement.append(df.at[index_of_max_value, 'CSLIP'])
    list_normal_force.append(df.at[index_of_max_value, 'CNORMF-Magnitude'])

df_rescue_hoist = pd.read_csv('Lasten/Rescue_Hoist_verteilt.csv')

df_rescue_hoist['Baseline CSLIP'] = list_relative_displacement
df_rescue_hoist['Baseline CNORMF_Magnitude'] = list_normal_force

df_rescue_hoist['Baseline Max Archard Wear'] = list_max_wear_archard
df_rescue_hoist['Baseline Max Fleischer Wear'] = list_max_wear_fleischer
df_rescue_hoist['Baseline Cumulative Max Archard Wear'] = df_rescue_hoist['Baseline Max Archard Wear'].cumsum()
df_rescue_hoist['Baseline Cumulative Max Fleischer Wear'] = df_rescue_hoist['Baseline Max Fleischer Wear'].cumsum()

for j in range(0, number_load_steps-1):
    if j == 0:
        load_duration = df_rescue_hoist['Time'].iloc[j]
        list_load_duration.append(load_duration/3600)

        load_change  = df_rescue_hoist['R'].iloc[j]
        list_load_change.append(abs(load_change))

    else:
        load_duration = df_rescue_hoist['Time'].iloc[j] - df_rescue_hoist['Time'].iloc[j-1]
        list_load_duration.append(load_duration / 3600)

        load_change = df_rescue_hoist['R'].iloc[j] - df_rescue_hoist['R'].iloc[j-1]
        list_load_change.append(abs(load_change))

df_rescue_hoist['R Change'] = list_load_change
df_rescue_hoist['Load Duration'] = list_load_duration

df_rescue_hoist.to_csv('Baseline/RescueHoist_Baseline.csv', index=False)
df_rescue_hoist.to_excel('Baseline/RescueHoist_Baseline.xlsx', index=False)


##

