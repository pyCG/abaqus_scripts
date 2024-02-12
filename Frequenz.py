

schalt = 10000
time = 4000

freq = schalt / (time*3600)
print(freq)

schalt_to_fail = 5.532e7
time_to_fail = schalt_to_fail /(freq*3600)
print(time_to_fail)

