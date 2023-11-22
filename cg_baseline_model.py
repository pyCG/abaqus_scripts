import pandas as pd


#path_rescue_hoist = 'D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model\FE-Scripts\FE-Inputs\Rescue_Hoist_verteilt.csv'
#df_rescue_hoist = pd.read_csv(path_rescue_hoist)

directory_folder = 'D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model\FE-Scripts\FE-Outputs'


list_max_wear_archard = []
list_max_wear_fleischer = []
list_mean_wear_archard = []
list_mean_wear_fleischer = []
list_relative_displacement = []
list_normal_force = []
number_load_steps = 1001
for i in range(1, number_load_steps):
    df = pd.read_csv(f'{directory_folder}\Calculated_Wear_Elements_Contact_Results_Job19_LP_{i}.csv')
    print(i)
    max_value_fleischer = df['Fleischer-Wear'].max()
    max_value_archard = df['Archard-Wear'].max()
    mean_value_fleischer = df['Fleischer-Wear'].mean()
    mean_value_archard = df['Archard-Wear'].mean()

    list_max_wear_archard.append(max_value_fleischer)
    list_max_wear_fleischer.append(max_value_archard)
    list_mean_wear_archard.append(mean_value_fleischer)
    list_mean_wear_fleischer.append(mean_value_archard)

    index_of_max_value = df[df['Fleischer-Wear'] == max_value_fleischer].index[0]

    list_relative_displacement.append(df.at[index_of_max_value, 'DELTA_CSLIP'])
    list_normal_force.append(df.at[index_of_max_value, 'DELTA_CNORMF-Magnitude'])

df_rescue_hoist = pd.read_csv('D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model\FE-Scripts\FE-Inputs\Rescue_Hoist_verteilt.csv')

df_rescue_hoist['DELTA_CSLIP'] = list_relative_displacement
df_rescue_hoist['DELTA_CNORMF_Magnitude'] = list_normal_force

df_rescue_hoist['Baseline Average Archard Wear'] = list_mean_wear_archard
df_rescue_hoist['Baseline Average Fleischer Wear'] = list_mean_wear_fleischer
df_rescue_hoist['Baseline Cumulative Average Archard Wear'] = df_rescue_hoist['Baseline Average Archard Wear'].cumsum()
df_rescue_hoist['Baseline Cumulative Average Fleischer Wear'] = df_rescue_hoist['Baseline Average Fleischer Wear'].cumsum()
df_rescue_hoist['Baseline Max Archard Wear'] = list_max_wear_archard
df_rescue_hoist['Baseline Max Fleischer Wear'] = list_max_wear_fleischer
df_rescue_hoist['Baseline Cumulative Max Archard Wear'] = df_rescue_hoist['Baseline Max Archard Wear'].cumsum()
df_rescue_hoist['Baseline Cumulative Max Fleischer Wear'] = df_rescue_hoist['Baseline Max Fleischer Wear'].cumsum()

df_rescue_hoist.to_csv('D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model\FE-Scripts\FE-Outputs\Rescue_Hoist_Wear_Verteilt.csv')
df_rescue_hoist.to_excel('D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model\FE-Scripts\FE-Outputs\Rescue_Hoist_Wear_Verteilt.xlsx')

#####TEST



