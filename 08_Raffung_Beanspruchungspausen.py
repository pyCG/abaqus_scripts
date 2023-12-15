##
import pandas as pd

df_voelligkeit = pd.read_csv('Voelligkeit/RescueHoist_Voelligkeit.csv')
df_pausen = pd.read_csv('Voelligkeit/RescueHoist_Voelligkeit.csv')
df_omission = pd.read_csv('Omission/RescueHoist_Omission_Threshold_17.csv')
df_baseline = pd.read_csv('Baseline/RescueHoist_Baseline.csv')

min_load_duration_minutes = 5 # minutes
max_load_duration_minutes = 60 # minutes

df_pausen.loc[df_pausen['Load Duration'] < min_load_duration_minutes/60, 'Load Duration'] = min_load_duration_minutes/60
df_pausen.loc[df_pausen['Load Duration'] >= max_load_duration_minutes/60, 'Load Duration'] = max_load_duration_minutes/60

baseline_test_duration = df_baseline['Load Duration'].cumsum().max()
omission_test_duration = df_omission['Load Duration'].cumsum().max()
voelligkeit_test_duration = df_voelligkeit['Load Duration'].cumsum().max()
pausen_test_duration = df_pausen['Load Duration'].cumsum().max()

print('----------------------------------------------------------------------------------')
print(f' | Baseline Duration: {baseline_test_duration:.1f}h | Omission Duration: {omission_test_duration:.1f}h | Voelligkeit Duration: {voelligkeit_test_duration:.1f}h | Beanspruchungspausen Duration: {pausen_test_duration:.1f}h |')

df_gerafftet_lastkollektiv = pd.DataFrame()
df_gerafftet_lastkollektiv['Time'] = df_pausen['Load Duration'].cumsum()
df_gerafftet_lastkollektiv['Time'] = df_gerafftet_lastkollektiv['Time']*3600
df_gerafftet_lastkollektiv = pd.concat([df_gerafftet_lastkollektiv['Time'], df_pausen[['MT1', 'MT2', 'MQF', 'FROX', 'FROY', 'FROZ', 'MROX', 'MROY', 'MROZ']]], axis=1)
df_gerafftet_lastkollektiv.to_csv('GeraffteLastkollektive/RescueHoist_gerafftes_Kollektiv_Beanspruchungspausen.csv', index=False)
df_gerafftet_lastkollektiv.to_excel('GeraffteLastkollektive/RescueHoist_gerafftes_Kollektiv_Beanspruchungspausen.xlsx', index=False)
