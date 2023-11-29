##
import pandas as pd
from cg_Wear_Archard_Fleischer_Plot import ARCHARD_wear_model
from cg_Wear_Archard_Fleischer_Plot import FLEISCHER_wear_model

last_frame = 1001  # Set this to the last frame number
k = 0.0001
H = 120
mu = 0.2
e_R = 100000

list_voelligkeit_archard = []
list_voelligkeit_fleischer = []
wear_difference_fleischer = -10e-6

df_voelligkeit = pd.read_csv('Omission/RescueHoist_Omission_Threshold_17.csv')
df_omission = pd.read_csv('Omission/RescueHoist_Omission_Threshold_17.csv')

df_voelligkeit = df_voelligkeit[df_voelligkeit['Load Duration'] < df_voelligkeit['Load Duration'].mean()]

df_voelligkeit_entfernt = df_voelligkeit[df_voelligkeit['Load Duration'] > df_voelligkeit['Load Duration'].mean()]

counter = 1

max_index = df_voelligkeit['Omission Max Fleischer Wear'].idxmax()
min_index = df_voelligkeit['Omission Max Fleischer Wear'].min()


average_value = df_voelligkeit['Omission Max Fleischer Wear'].mean()
mean_index = (df_voelligkeit['Omission Max Fleischer Wear'] - average_value).abs().idxmin()

nearest_row_min = df_voelligkeit.loc[mean_index]
nearest_row_max = df_voelligkeit.loc[max_index]

while wear_difference_fleischer < 0:
    list_voelligkeit_archard = []
    list_voelligkeit_fleischer = []

    df_voelligkeit = pd.concat([pd.DataFrame([nearest_row_min], columns=df_voelligkeit.columns), df_voelligkeit],
                               ignore_index=True)
    df_voelligkeit = pd.concat([pd.DataFrame([nearest_row_max], columns=df_voelligkeit.columns), df_voelligkeit],
                               ignore_index=True)

    for i in range(0, len(df_voelligkeit)):

        index_normal_force = df_voelligkeit.columns.get_loc('Baseline CNORMF_Magnitude')
        index_relative_displacement = df_voelligkeit.columns.get_loc('Baseline CSLIP')

        if i == 0:
            p_A = [df_voelligkeit.iat[i, index_normal_force] / 2]
            s = [df_voelligkeit.iat[i, index_relative_displacement]]

            wear_archard = ARCHARD_wear_model(p_A=p_A,
                                              s=s,
                                              k=k,
                                              H=H)
            list_voelligkeit_archard.append(wear_archard[0])

            wear_fleischer = FLEISCHER_wear_model(p_A=p_A,
                                                  s=s,
                                                  mu=mu,
                                                  e_R=e_R)
            list_voelligkeit_fleischer.append(wear_fleischer[0])

        else:
            p_A = [(df_voelligkeit.iat[i, index_normal_force] + df_voelligkeit.iat[i - 1, index_normal_force]) / 2]
            s = [df_voelligkeit.iat[i, index_relative_displacement] - df_voelligkeit.iat[
                i - 1, index_relative_displacement]]

            wear_archard = ARCHARD_wear_model(p_A=p_A,
                                              s=s,
                                              k=k,
                                              H=H)
            list_voelligkeit_archard.append(wear_archard[0])

            wear_fleischer = FLEISCHER_wear_model(p_A=p_A,
                                                  s=s,
                                                  mu=mu,
                                                  e_R=e_R)
            list_voelligkeit_fleischer.append(wear_fleischer[0])
    counter = counter + 1

    wear_omission_fleischer = df_omission['Baseline Max Fleischer Wear'].cumsum().max()
    wear_voelligkeit_fleischer = sum(list_voelligkeit_fleischer)

    wear_difference_fleischer = (wear_voelligkeit_fleischer - wear_omission_fleischer) * 100 / wear_omission_fleischer

    voelligkeit_test_duration = df_voelligkeit['Load Duration'].cumsum().max()
    omission_test_duration = df_omission['Load Duration'].cumsum().max()

    print('----------------------------------------------------------------------------------')
    print(
        f' {counter} | Wear difference: {wear_difference_fleischer:.2f} % | Omission: {wear_omission_fleischer:.6f} | Voelligkeit: {wear_voelligkeit_fleischer:.6f} | Omission Duration: {omission_test_duration:.1f}h | Voelligkeit Duration: {voelligkeit_test_duration:.1f}h | ')

##
