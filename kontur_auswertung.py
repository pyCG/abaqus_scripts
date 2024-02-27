import matplotlib.pyplot as plt
from decimal import Decimal

# Funktion zum Plotten und Speichern einer Datei
def plot_and_save(reference_filename, compare_filename, save_filename):
    x_ref = []
    y_ref = []
    x_cmp = []
    y_cmp = []

    # Öffnen und Lesen der Referenzdatei
    try:
        with open(reference_filename, 'r') as ref_file:
            # Ignoriere die ersten beiden Zeilen
            next(ref_file)
            next(ref_file)

            # Lese die X- und Y-Werte aus den verbleibenden Zeilen
            x_transformiert = Decimal('0')
            for line in ref_file:
                x, y, _ = line.split()
                x_float = float(x_transformiert)
                if x_float <= 21.0:  # Überprüfe, ob x_transformiert kleiner oder gleich 21.0 ist
                    x_ref.append(x_float)
                    y_ref.append(float(y))
                x_transformiert += Decimal('0.0005')

        # Öffnen und Lesen der Vergleichsdatei
        with open(compare_filename, 'r') as cmp_file:
            # Ignoriere die ersten beiden Zeilen
            next(cmp_file)
            next(cmp_file)

            # Lese die X- und Y-Werte aus den verbleibenden Zeilen
            x_transformiert = Decimal('0')
            for line in cmp_file:
                x, y, _ = line.split()
                x_float = float(x_transformiert)
                if x_float <= 21.0:  # Überprüfe, ob x_transformiert kleiner oder gleich 21.0 ist
                    x_cmp.append(x_float)
                    y_cmp.append(float(y))
                x_transformiert += Decimal('0.0005')

        # Plot erstellen
        plt.figure(figsize=(10, 6))

        # Plot der blauen und roten Kurve
        plt.subplot(2, 1, 1)
        plt.plot(x_ref, y_ref*10**3, color='blue', label=f'Messung'+compare_filename[7:9])
        plt.plot(x_cmp, y_cmp*10**3, color='red', label=f'Messposition {int(compare_filename[7:9]) * 5.6:.1f} Grad')
        plt.xlabel('Xtransformiert / mm')
        plt.ylabel('Profilhöhe / µm')
        plt.title(f'Profilhöhe über Xtaststr. ({compare_filename[:-4]} vs. Messung01)')
        plt.grid(True)
        plt.legend()

        # Plot der Differenz zwischen den Kurven
        plt.subplot(2, 1, 2)
        plt.plot(x_ref, [y1 - y2 for y1, y2 in zip(y_ref, y_cmp)], color='green', label='Differenz')
        plt.xlabel('Xtransformiert [mm]')
        plt.ylabel('Differenz')
        plt.title('Differenz zwischen den Kurven')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.savefig(save_filename)  # Speichern der Grafik als Bilddatei
        plt.close()  # Schließen des aktuellen Diagramms, um Speicherplatz zu sparen
    except FileNotFoundError:
        print(f"Die Datei wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten:", e)


# Vergleiche Messung01 mit den ersten 64 Messungen
for i in range(1, 65):
    reference_filename = "KonturVermessung/Messung01.txt"
    compare_filename = f"KonturVermessung/Messung{i:02}.txt"
    print(compare_filename)
    save_filename = f"WearResults/Kontur_Vergleich_Messung01_{compare_filename[:-4]}.png"
    plot_and_save(reference_filename, compare_filename, save_filename)

