import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import os
import numpy as np

def plot_and_save(reference_filename, compare_filename, save_filename, folder_path, folder_path_ref):
    df_referenz = pd.read_csv(folder_path_ref + '/' + reference_filename, skiprows=2, sep=r'\t', header=None,
                              engine='python')
    df_vermessung = pd.read_csv(folder_path + '/' + compare_filename, skiprows=2, sep=r'\t', header=None,
                                engine='python')
    x_ref = df_referenz[0]
    y_ref = df_referenz[1]
    x_cmp = df_vermessung[0]
    y_cmp = df_vermessung[1]

    x_ref = x_ref - min(x_ref)
    index_x_ref = x_ref[x_ref < 21].idxmax()

    x_ref = x_ref.loc[:index_x_ref]
    y_ref = y_ref.loc[:index_x_ref]

    x_cmp = x_cmp - min(x_cmp)
    index_x_cmp = x_cmp[x_cmp < 21].idxmax()

    x_cmp = x_cmp.loc[:index_x_cmp]
    y_cmp = y_cmp.loc[:index_x_cmp]

    len_x_ref = len(y_ref)
    len_x_cmp = len(y_cmp)

    if len_x_ref > len_x_cmp:
        x_ref = x_ref[:len_x_cmp]  # Truncate
        y_ref = y_ref[:len_x_cmp]
    elif len_x_cmp > len_x_ref:
        x_cmp = x_cmp[:len_x_ref]  # Truncate
        y_cmp = y_cmp[:len_x_ref]

    # Calculate wear
    y_wear = (y_ref - y_cmp) * 10 ** 3
    print(y_ref.max())
    print(y_cmp.max())

    # define the true objective function
    def objective(x, a, b, c, d, e, f):
        return (a * x) + (b * x ** 2) + (c * x ** 3) + (d * x ** 4) + (e * x ** 5) + f

    # curve fit
    popt, _ = curve_fit(objective, x_ref, y_wear)
    # summarize the parameter values
    a, b, c, d, e, f = popt
    y_wear_fit = objective(x_ref, a, b, c, d, e, f)

    # Define blue colors in RGB format (normalized)
    blue1 = (0 / 255, 84 / 255, 159 / 255)  # Oxford Blue (0x00549F)
    blue2 = (64 / 255, 127 / 255, 183 / 255)  # Glaucous (0x407FB7)
    blue3 = (142 / 255, 186 / 255, 229 / 255)  # Baby Blue (0x8EBAE5)
    blue4 = (199 / 255, 221 / 255, 242 / 255)  # Powder Blue (0xC7DDF2)
    blue5 = (232 / 255, 241 / 255, 250 / 255)  # Alice Blue (0xE8F1FA)
    # Define orange colors in RGB format (normalized)
    orange1 = (246 / 255, 168 / 255, 0 / 255)  # Dark Orange (0xF6A800)
    orange2 = (250 / 255, 190 / 255, 80 / 255)  # Macaroni and Cheese (0xFABE50)
    orange3 = (253 / 255, 212 / 255, 143 / 255)  # Peach Puff (0xFDD48F)
    orange4 = (254 / 255, 234 / 255, 201 / 255)  # Apricot (0xFEEAC9)
    orange5 = (255 / 255, 247 / 255, 234 / 255)  # Floral White (0xFFF7EA)

    # Define green colors in RGB format (normalized)
    green1 = (87 / 255, 171 / 255, 39 / 255)  # Leaf Green (0x57AB27)
    green2 = (141 / 255, 192 / 255, 96 / 255)  # Mantle (0x8DC060)
    green3 = (184 / 255, 214 / 255, 152 / 255)  # Granny Smith Apple (0xB8D698)
    green4 = (221 / 255, 235 / 255, 206 / 255)  # Very Pale Green (0xDDEBCE)
    green5 = (242 / 255, 247 / 255, 236 / 255)  # Ivory (0xF2F7EC)

    # Plot erstellen
    plt.figure(figsize=(10, 6))

    # Plot der blauen und roten Kurve
    plt.subplot(2, 1, 1)
    plt.plot(x_ref, (y_ref - math.floor(max(y_ref)))*10**3, color=blue1, label=f'Referenz - Messung {reference_filename[7:9]}')
    plt.plot(x_cmp, (y_cmp - math.floor(max(y_cmp)))*10**3, color=blue3, label=f'Messung {compare_filename[7:9]} - {int(compare_filename[7:9]) * 5.6:.1f} Grad')
    plt.xlabel('Außenringbreite / mm')
    plt.ylabel('Profilhöhe / µm')
    plt.title(f'Profilhöhe ({compare_filename[:-4]} vs. Messung'+reference_filename[7:9] + ' - Referenz)')
    plt.grid(True)
    plt.legend()

    # Plot der Differenz zwischen den Kurven
    plt.subplot(2, 1, 2)
    plt.plot(x_ref, y_wear, color=green1, label = f'Referenz - Messung (Maxwert={y_wear.max():.2f} Durchschnitt={y_wear.mean():.2f})')
    plt.plot(x_ref, y_wear_fit, color=orange1, label=f'Fitted Curve (Maxwert={y_wear_fit.max():.2f} Durchschnitt={y_wear_fit.mean():.2f})')
    plt.xlabel('Außenringbreite / mm')
    plt.ylabel('Verschleißtiefe / µm')
    plt.title('Verschleiß an der Ringbreite')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig(save_filename)  # Speichern der Grafik als Bilddatei
    plt.close()  # Schließen des aktuellen Diagramms, um Speicherplatz zu sparen



def count_txt_files(folder_path):
    txt_count = 0
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            txt_count += 1
    return txt_count
folder_path_ref = '5GradMessung(erste)'
folder_path = '30GradMessungen'
txt_file_count = count_txt_files(folder_path)

# Vergleiche Messung01 mit den ersten 64 Messungen
for i in range(1, txt_file_count+1):
    reference_filename = "Messung02.txt"
    compare_filename = f"Messung30-{i}.txt"
    print(compare_filename)
    save_filename = f"WearResults - 30 Grad/Kontur_Vergleich_Messung01_{compare_filename[:-4]}.png"
    plot_and_save(reference_filename, compare_filename, save_filename, folder_path,folder_path_ref)