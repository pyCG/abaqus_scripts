##
#rotation = 1696 #rpm
total_time = 4000 # h
cycles_to_fail_manfred = 3.25e7 # n# cycles

frequency = 0.0006944
#frequency = rotation / 60
print(f"Frequency: {frequency:.2f} Hz")

cycles = frequency * total_time * 3600
print(f"Cycles in 4000h: {cycles:.2e}")
print(f"Cycles to fail with a 99% Probability: {cycles_to_fail_manfred:.2e}")

time_to_manfred_cycles = cycles_to_fail_manfred/(frequency*3600)
print(f"Flight hours with a 99% Probability: {time_to_manfred_cycles:.2e} h")
