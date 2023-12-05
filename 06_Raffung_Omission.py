##
import pandas as pd
from cg_Wear_Archard_Fleischer_Plot import ARCHARD_wear_model
from cg_Wear_Archard_Fleischer_Plot import FLEISCHER_wear_model
import warnings

warnings.filterwarnings("ignore")
df_baseline = pd.read_csv('Baseline/RescueHoist_Baseline.csv')

last_frame = 1001  # Set this to the last frame number
k = 0.0001
H = 120
mu = 0.2
e_R = 100000
thresholds = [1, 2, 5, 6, 7, 8, 9, 10, 15, 16, 17, 18, 19, 20]

print('OMISSION OF SMALL LOAD CHANGE AMPLITUDES')
print('==================================================================================')
for threshold in thresholds:
    # df_omission = df_baseline[df_baseline['R'] >= df_baseline['R'].max() * (threshold/100)]
    df_omission = df_baseline[df_baseline['R Change'] >= df_baseline['R Change'].max() * (threshold / 100)]
    min_force = df_baseline['R Change'].max() * (threshold / 100)
    print(f' Threshold Change of Force: {min_force:.2f} N')
    list_omission_archard = []
    list_omission_fleischer = []

    for i in range(0, len(df_omission)):

        index_normal_force = df_omission.columns.get_loc('Baseline CNORMF_Magnitude')
        index_relative_displacement = df_omission.columns.get_loc('Baseline CSLIP')

        if i == 0:
            p_A = [df_omission.iat[i, index_normal_force] / 2]
            s = [df_omission.iat[i, index_relative_displacement]]

            wear_archard = ARCHARD_wear_model(p_A=p_A,
                                              s=s,
                                              k=k,
                                              H=H)
            list_omission_archard.append(wear_archard[0])

            wear_fleischer = FLEISCHER_wear_model(p_A=p_A,
                                                  s=s,
                                                  mu=mu,
                                                  e_R=e_R)
            list_omission_fleischer.append(wear_fleischer[0])

        else:
            p_A = [(df_omission.iat[i, index_normal_force] + df_omission.iat[i - 1, index_normal_force]) / 2]
            s = [df_omission.iat[i, index_relative_displacement] - df_omission.iat[i - 1, index_relative_displacement]]

            wear_archard = ARCHARD_wear_model(p_A=p_A,
                                              s=s,
                                              k=k,
                                              H=H)
            list_omission_archard.append(wear_archard[0])

            wear_fleischer = FLEISCHER_wear_model(p_A=p_A,
                                                  s=s,
                                                  mu=mu,
                                                  e_R=e_R)
            list_omission_fleischer.append(wear_fleischer[0])

    df_omission['Omission Max Archard Wear'] = list_omission_archard
    df_omission['Omission Max Fleischer Wear'] = list_omission_fleischer
    max_omission_wear_archard = df_omission['Omission Max Archard Wear'].cumsum().max()
    max_omission_wear_fleischer = df_omission['Omission Max Fleischer Wear'].cumsum().max()

    max_baseline_wear_archard = df_baseline['Baseline Max Archard Wear'].cumsum().max()
    max_baseline_wear_fleischer = df_baseline['Baseline Max Fleischer Wear'].cumsum().max()

    wear_difference_archard = (max_baseline_wear_archard - max_omission_wear_archard) * 100 / max_baseline_wear_archard
    wear_difference_fleischer = (max_baseline_wear_fleischer - max_omission_wear_fleischer) * 100 / max_baseline_wear_fleischer

    total_time_baseline = df_baseline['Load Duration'].sum()
    total_time_omission = df_omission['Load Duration'].sum()
    reduced_time = total_time_baseline - total_time_omission

    permissible_wear_difference_percentage = 10
    if wear_difference_archard <= permissible_wear_difference_percentage:
        print(
            f' VALID | Wear Difference: {wear_difference_archard:.2f}% < 10% | Reduced Time: {reduced_time:.2f}h | Remaining Time: {total_time_omission:.2f}h | Threshold: {threshold}% |  ')
        print('----------------------------------------------------------------------------------')

        df_omission.to_csv(f'Omission/RescueHoist_Omission_Threshold_{threshold}.csv', index=False)
        df_omission.to_excel(f'Omission/RescueHoist_Omission_Threshold_{threshold}.xlsx', index=False)

    else:
        print(
            f' INVALID | Wear Difference: {wear_difference_archard:.2f}% < 10% | Reduced Time: {reduced_time:.2f}h | Remaining Time: {total_time_omission:.2f}h | Threshold: {threshold}% | ')
        print('----------------------------------------------------------------------------------')
##
