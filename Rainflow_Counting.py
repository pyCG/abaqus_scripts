##
import pandas as pd
def rainflow_counting(data):
    """
    Rainflow counting method to count cycles in a load history.

    Parameters:
    - data: 1D array representing the load history.

    Returns:
    - cycles: List of dictionaries, each containing 'range' and 'mean' values.
    """
    cycles = []

    n = len(data)
    i = 0

    while i < n - 2:
        if data[i] < data[i + 1] > data[i + 2]:  # Upturn
            j = i + 1
            while j < n - 1 and data[j] <= data[j + 1]:
                j += 1
            cycles.append({'range': data[i + 1] - data[i], 'mean': (data[i + 1] + data[i]) / 2})
            i = j
        elif data[i] > data[i + 1] < data[i + 2]:  # Downturn
            j = i + 1
            while j < n - 1 and data[j] >= data[j + 1]:
                j += 1
            cycles.append({'range': data[i] - data[i + 1], 'mean': (data[i] + data[i + 1]) / 2})
            i = j
        else:
            i += 1

    return cycles


# Example usage:

header = ['Fy','Fz','Time','MT1','MT2','MQF','FROX','FROY','FROZ','MROX','MROY','MROZ']
df = pd.read_csv('Lasten/Rescue_Hoist_Forces_unverteilt.csv', header=None, names=header)
load_history = df["MT2"]

#load_history = [0, 2, -1, 3, -2, 1, -1, 4, 0, -3]
rainflow_cycles = rainflow_counting(load_history)

# Display the counted cycles
print("Rainflow counted cycles:")
for cycle in rainflow_cycles:
    print(f"Range: {cycle['range']}, Mean: {cycle['mean']}")

print(f"Number of cycles in 4000h: {len(rainflow_cycles)*28} cycles")
