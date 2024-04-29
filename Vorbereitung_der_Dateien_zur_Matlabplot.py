import pandas as pd


#### Use victrex script for wear and roughness plots

index = [1, 8, 14, 25, 28, 32, 36, 39, 50, 56]
let = ['b', 'f', 'm']
for j in range(0, len(let)):
    for i in range(0, len(index)):
        # Read the input file
        input_file = f"D:\MoVerHu_Projekt\Messungen Carlos\Matlab\Rauheit\Messung{index[i]}.txt"

        df = pd.read_csv(input_file, delimiter='\t')

        # Rename the columns
        df.columns = ['X', 'Y', 'Gültig']

        # Add a new column 'Anzahl'
        df.insert(0, 'Anzahl', range(len(df)))

        # Reorder the columns
        df = df[['Anzahl', 'X', 'Y', 'Gültig']]

        # Write the transformed dataframe to a new file
        output_file = f"D:\MoVerHu_Projekt\Messungen Carlos\Matlab\Rauheit\_Messung{index[i]}_{let[j]}.txt"
        df.to_csv(output_file, sep='\t', index=False)

        print("Transformation completed. Output saved to", output_file)

