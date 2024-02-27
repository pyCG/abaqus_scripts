##

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
##

def extract_start_x(file_path):
    """
    Extract the value associated with the key "START_X" from the [PROFILE_HEADER] section of a file.

    Parameters:
    - file_path (str): Path to the file to be processed.

    Returns:
    - start_x_value (float or None): Value of START_X if found, None otherwise.
    """
    # Initialize variables
    in_profile_header = False
    start_x_value = None
    print(file_path)
    # Open the file in read mode
    with open(file_path, "r") as file:
        # Iterate through each line in the file
        for line in file:
            # Strip whitespace from the beginning and end of the line
            line = line.strip()

            # Check if the line marks the beginning of the [PROFILE_HEADER] section
            if line == "[PROFILE_HEADER]":
                # Set the flag to indicate that we're in the [PROFILE_HEADER] section
                in_profile_header = True
            # Check if the line marks the beginning of another section or if it's empty
            elif line.startswith("[") or not line:
                # Set the flag to indicate that we're not in the [PROFILE_HEADER] section anymore
                in_profile_header = False
            # If we're in the [PROFILE_HEADER] section
            elif in_profile_header:
                # Split the line by '=' to separate the key and the value
                key, value = line.split("=")
                # Check if the key is START_X
                if key.strip() == "START_X":
                    # Store the value in the variable
                    start_x_value = float(value.strip())
                    # No need to continue iterating through the file, as we found what we needed
                    break

    # Return the extracted START_X value
    return start_x_value

##
for i in range(0, 9):

    # Read the first file into a DataFrame, skipping 52 rows, treating spaces as separators, without a header, and using latin1 encoding
    file_path_new = f'Measurements/moverhu_04_rundheit_nicht_0{i+1}.txt'
    file_path_gelaufen = f'Measurements/moverhu_04_rundheit_gelaufen_0{i+1}.txt'

    df_new = pd.read_csv(file_path_new, skiprows=52, sep=' ', header=None, index_col=False, encoding='latin1')
    # Read the second file into a DataFrame using similar settings
    df_gelaufen = pd.read_csv(file_path_gelaufen, skiprows=52, sep=' ', header=None, index_col=False, encoding='latin1')

    # Define column names for the DataFrames
    columns = ['X', 'Y', 'Z', 'C', 'Lock']
    # Assign column names to the DataFrames
    df_new.columns = columns
    df_gelaufen.columns = columns

    # Extract the numeric value from the 'X' column by splitting on '=' and converting to numeric type
    df_new['X'] = df_new['X'].str.split('=').str.get(1)
    df_new['X'] = pd.to_numeric(df_new['X'])

    # Extract the numeric value from the 'X' column of the second DataFrame in a similar manner
    df_gelaufen['X'] = df_gelaufen['X'].str.split('=').str.get(1)
    df_gelaufen['X'] = pd.to_numeric(df_gelaufen['X'])

    # Extract X and Y coordinates from the first DataFrame
    x_new = df_new['X']
    y_new = df_new['Y']

    # Convert Cartesian coordinates to polar coordinates (radius and angle) for the first DataFrame
    r_new = np.sqrt(x_new**2 + y_new**2)
    theta_new = np.arctan2(y_new, x_new)
    theta_new = np.where(theta_new < 0, theta_new + 2*np.pi, theta_new)  # Ensure angles are in [0, 2*pi]

    # Extract X and Y coordinates from the second DataFrame
    x_gelaufen = df_gelaufen['X']
    y_gelaufen = df_gelaufen['Y']

    # Convert Cartesian coordinates to polar coordinates (radius and angle) for the second DataFrame
    r_gelaufen = np.sqrt(x_gelaufen**2 + y_gelaufen**2)
    theta_gelaufen = np.arctan2(y_gelaufen, x_gelaufen)
    theta_gelaufen = np.where(theta_gelaufen < 0, theta_gelaufen + 2*np.pi, theta_gelaufen)  # Ensure angles are in [0, 2*pi]

    # Call reference

    start_x_new = abs(extract_start_x(file_path_new))
    start_x_gelaufen = abs(extract_start_x(file_path_gelaufen))
    print("START_X RU - Referenz, wenig veschlissen", start_x_new)
    print("START_X LU gelaufen:", start_x_gelaufen)

    # Create a scatter plot
    fig, ax = plt.subplots()
    # Adjusting the radius by subtracting a constant

    ax.scatter(theta_new, r_new-start_x_new, label='RU - Referenz, wenig veschlissen', s=1)
    ax.scatter(theta_new, r_gelaufen-start_x_gelaufen, label='LU - gelaufen:', s=1)
    ax.set_xticks(np.linspace(0, 2*np.pi, 9))  # Set the ticks on the x-axis to be evenly spaced angles in radians
    ax.set_xticklabels([f'{int(np.degrees(theta))}°' for theta in np.linspace(0, 2*np.pi, 9)])  # Convert radians to degrees for tick labels

    # Add axis labels
    ax.set_xlabel('Winkel / Grad')
    ax.set_ylabel('Durchmesserdifferenz / mm')

    # Move the legend to the top-right corner
    ax.legend(loc='upper center')
    ax.grid()  # Add grid lines
    plt.legend()  # Show legend
    fig.savefig(f'WearResults/wear_{i+1}.png')  # Save the plot as an image file


