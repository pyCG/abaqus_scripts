import pandas as pd


#path_rescue_hoist = 'D:\MoVerHu_Projekt\FE_Modell\FE-Abaqus-Model\FE-Scripts\FE-Inputs\Rescue_Hoist_verteilt.csv'
#df_rescue_hoist = pd.read_csv(path_rescue_hoist)

path_test = 'CalculatedWear.csv'


list_wear_archard = []
list_wear_fleischer = []
list_relative_displacement = []
list_normal_force = []
for i in range(1, 1001):
    df = pd.read_csv(path_test)

    max_value_fleischer = df['Fleischer-Wear'].max()
    max_value_archard = df['Archard-Wear'].max()

    list_wear_archard.append(max_value_fleischer)
    list_wear_fleischer.append(max_value_archard)

    index_of_max_value = df[df['Fleischer-Wear'] == max_value_fleischer].index[0]

    list_relative_displacement.append(df.at[index_of_max_value, 'DELTA_CSLIP'])
    list_normal_force.append(df.at[index_of_max_value, 'DELTA_CNORMF-Magnitude'])


df_rescue_hoist = pd.DataFrame()
df_rescue_hoist['DELTA_CSLIP'] = list_relative_displacement
df_rescue_hoist['DELTA_CNORMF_Magnitude'] = list_normal_force
df_rescue_hoist['Baseline Max Archard Wear'] = list_wear_archard
df_rescue_hoist['Baseline Max Fleischer Wear'] = list_wear_fleischer
df_rescue_hoist['Baseline Cumulative Archard Wear'] = df_rescue_hoist['Baseline Max Archard Wear'].cumsum()
df_rescue_hoist['Baseline Cumulative Fleischer Wear'] = df_rescue_hoist['Baseline Max Fleischer Wear'].cumsum()



