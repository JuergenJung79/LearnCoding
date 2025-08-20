import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

CSV_FILE = 'daten.csv'

# Initialisiere CSV, falls nicht vorhanden
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Datum', 'Gewicht', 'Kacka'])

# Daten eingeben
def daten_eingeben():
    datum = input("Datum (YYYY-MM-DD): ")
    try:
        datetime.strptime(datum, "%Y-%m-%d")
    except ValueError:
        print("Ungültiges Datum.")
        return

    gewicht = input("Gewicht (in kg): ")
    try:
        gewicht = float(gewicht)
    except ValueError:
        print("Ungültiges Gewicht.")
        return

    kacka = input("Kacka (ja/nein): ").lower()
    if kacka not in ['ja', 'nein']:
        print("Ungültiger Eintrag für Kacka.")
        return

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datum, gewicht, kacka])
    print("✅ Daten gespeichert.")

# Daten anzeigen & visualisieren
def daten_visualisieren():
    daten = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                datum = datetime.strptime(row['Datum'], "%Y-%m-%d")
                gewicht = float(row['Gewicht'])
                kacka = 1 if row['Kacka'].lower() == 'ja' else 0
                daten.append((datum, gewicht, kacka))
            except Exception as e:
                print("Fehler beim Verarbeiten einer Zeile:", e)

    if not daten:
        print("Keine Daten vorhanden.")
        return

    daten.sort(key=lambda x: x[0])  # Nach Datum sortieren

    daten_liste, gewicht_liste, kacka_liste = zip(*daten)

    # Gewichtslinie
    plt.figure(figsize=(10, 5))
    plt.plot(daten_liste, gewicht_liste, marker='o', label='Gewicht (kg)')
    
    # Kacka als Punkte
    kacka_daten = [d for i, d in enumerate(daten_liste) if kacka_liste[i] == 1]
    kacka_gewicht = [gewicht_liste[i] for i, d in enumerate(daten_liste) if kacka_liste[i] == 1]
    plt.scatter(kacka_daten, kacka_gewicht, color='red', label='Kacka = ja')

    plt.xlabel("Datum")
    plt.ylabel("Gewicht (kg)")
    plt.title("Gewichtsentwicklung mit Kacka-Marker")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Menü
def menue():
    init_csv()
    while True:
        print("\n--- Menü ---")
        print("1. Neue Daten eingeben")
        print("2. Daten visualisieren")
        print("3. Beenden")
        wahl = input("Auswahl: ")

        if wahl == '1':
            daten_eingeben()
        elif wahl == '2':
            daten_visualisieren()
        elif wahl == '3':
            print("Programm beendet.")
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    menue()
